from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.http import Http404
from rest_framework import permissions

from django.contrib.auth.models import User

def indexView(request):
    return render(request,'index.html')

class ProductView(APIView):

    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Product.objects.all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)


class ShopProductView(APIView):

    """
    List all snippets, or create a new snippet.
    """
    def get(self, request,category, format=None):
        snippets = Product.objects.filter(category = category)
        serializer = ShopProductSerializer(snippets, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get_object(self, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404


    def get(self, request,slug, format=None):
        snippets = self.get_object(slug)
        serializer = ProductSerializer(snippets)
        return Response(serializer.data)



class CartView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        # print(request.user.id)
        try:
            order = Order.objects.get(customer = request.user.id,complete = False)
            if order.complete is not True:
                snippets = OrderItem.objects.filter(order = order)
                serializer = OrderItemSerializer(snippets, many=True)
                data = serializer.data
            else :
                data = []
        except :
            data = []  # send back empty array coz i have done map in the frontend

        return Response(data)

    def post(self, request, format=None):
        data = self.request.data
        productId = data['id']
        action = data['action']


        user = User.objects.get(username = request.user)
        customer,created = Customer.objects.get_or_create(user= user, name = request.user.username ,email = request.user.email)

        order,created = Order.objects.get_or_create(customer = customer, complete = False)

        
        product = Product.objects.get(id = productId)
        
        orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
 
        if action == 'add':
            orderItem.quantity = orderItem.quantity + 1

        elif action == 'remove':
            orderItem.quantity = orderItem.quantity -1

        orderItem.save()

        if orderItem.quantity <=0:
            orderItem.delete()

        return Response('successful' ,status=status.HTTP_201_CREATED)


class OrderView(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):

        try:
            order = Order.objects.get(customer = request.user.id, complete = False)
            serializer = OrderSerializer(order)
            data = serializer.data
        except :
            data = []

        return Response(data)


class ShippingView(APIView):

    def post(self,request,format = None):
        customer =Customer.objects.get(user = request.user.id)
        try:
            order = Order.objects.get(customer = request.user.id,complete = False)
            newRequest = {
            'customer' :customer.id,
            'order' : order.id
            }
            newRequest = {**newRequest,**request.data}
            serializer = ShippingSerializer(data = newRequest)
            if serializer.is_valid():
                serializer.save()
                order.complete = True
                order.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'Thats bad mate'},status.HTTP_400_BAD_REQUEST )
        except :
            return Response({'Thats bad mate'},status.HTTP_400_BAD_REQUEST )
            

class RecomView(APIView):
    def get(self,request,format = None):

        snippets = Recom.objects.all()
        serializer = RecomSerializer(snippets, many=True)
        return Response(serializer.data)

class CommentView(APIView):
    def get(self,request,format = None):
        # print(request.query_params.get('id'))
        snippets = Comment.objects.filter(product = request.query_params.get('id'))
        serializer = CommentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self,request,format = None):
        customer =Customer.objects.get(user = request.user.id)
        
        newRequest = {
            'person' : customer.id,
        }

        newRequest = {**request.data,**newRequest,}
        serializer = CommentSerializer(data= newRequest)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status.HTTP_400_BAD_REQUEST )

        
