
from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name='index'),
    path('products/', ProductView.as_view()),
    path('cartitems/', CartView.as_view()),
    path('orders/', OrderView.as_view()),
    path('shipping/', ShippingView.as_view()),
    path('recom/', RecomView.as_view()),
    path('comment/', CommentView.as_view()),
    path('products/<slug>/', ProductDetailView.as_view()),
    
    path('shop/<category>/', ShopProductView.as_view()),

    
]
