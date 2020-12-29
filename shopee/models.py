from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True, blank = True)
    name = models.CharField(max_length = 200, null =True)
    email = models.CharField(max_length = 200, null =True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CHOICES = (
    ('summer', 'summer'),
    ('winter', 'winter'),
    )
    name = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits= 7, decimal_places=2)
    # digital = models.BooleanField(default=False,null= True, blank = False)
    # image = models.ImageField(null= True, blank = True)
    category = models.CharField(max_length=30, choices = CHOICES)
    desc = models.TextField(null= False, blank = False)
    slug = models.SlugField()

# this is done to make sure if no image is added then no error occurs
    # @property 
    # def imageURL(self):
    #     try:
    #         url = "http://reactshopee.herokuapp.com" +self.image.url
    #     except:
    #         url = ""
        
    #     return url

    # @property
    # def product_quantity(self):
    #     quantity = 

    # override the slug field to make it unique
    def save(self,*args, **kwargs):
        original_slug = slugify(self.name)
        queryset = Product.objects.all().filter(slug__iexact = original_slug).count()  # count the no of items with same slug

        count = 1
        slug = original_slug 

        while(queryset):  # if there is any queryset, i.e while(1), if not queryset then it becomes while(0) so this part will be skipped
            slug = original_slug + "-" + str(count)
            count += 1 
            queryset = Product.objects.all().filter(slug__iexact = slug).count()  # count the no of items with same slug
 
        self.slug = slug

        super(Product,self).save(*args, **kwargs)


    def __str__(self):
        return self.name
       
class ProductImage(models.Model):
    
    def generate_filename(self, filename):
        url = "imgs/%s/%s" % (self.product.name, filename)
        return url

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to=generate_filename)

    def __str__(self):
        return str(f"{self.product}---{self.id}")   

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null= True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null= True, blank = False)
    transaction_id = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.id)

    @property # to check if the transaction is digital
    def shipping(self):
        shipping = False
        OrderItems = self.orderitem_set.all() #order is related one-many with OrderItems
        for i in OrderItems:
            if i.product.digital == False:
                shipping = True
        
        return shipping

    @property 
    def get_cart_total(self):
        orderItems = self.orderitem_set.all()  # we have done this in views too
        total = sum([item.get_total for item in orderItems])
        return total
    
    @property 
    def get_cart_items(self):
        orderItems = self.orderitem_set.all()  # we have done this in views too
        total = sum([item.quantity for item in orderItems])
        return total


class OrderItem(models.Model): 
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null= True, blank = True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null= True, blank = True)
    quantity = models.IntegerField(default=0,null= True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name + '--' + str( self.order))


    @property
    def get_total(self):
        total =self.product.price * self.quantity
        return total

    @property
    def get_item_name(self):
        name = self.product.name 
        return name

    @property
    def get_item_price(self):
        price = self.product.price 
        return price


    @property
    def get_item_img(self):
        img = self.product.imageURL 
        return img


class Shipping(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null= True, blank = True )
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null= True, blank = True )
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    state = models.CharField(max_length = 200, null = True)
    zipcode = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


class Recom(models.Model):
    recoName = models.CharField(max_length = 200,)
    recoPost = models.CharField(max_length = 200,)
    recoText = models.TextField(null= False, blank = False)
    recoImg = models.ImageField() 

    @property 
    def recoImageURL(self):
        try:
            url = "http://127.0.0.1:8000" +self.recoImg.url
        except:
            url = ""
        
        return url

    def __str__(self):
        return str(self.recoName)

class Comment(models.Model):
    person = models.ForeignKey(Customer,on_delete=models.CASCADE,null= True, blank = True )
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null= True, blank = True)
    comment_added = models.DateTimeField(auto_now_add=True)
    commentText = models.TextField(null= False, blank = False)
    

    @property
    def get_person_name(self):
        name = self.person.name 
        return name

    def __str__(self):
        return str(self.product.name)