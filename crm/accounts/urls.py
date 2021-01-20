from django.urls import path,include
from . import views

urlpatterns = [
    path('login/' ,views.loginpage,name="login"),
    path('logout/' ,views.logoutuser,name="logout"),
    path('register/',views.registerpage,name="register"),
    
    path('user/',views.userpage,name="user-page"),
    path('account/', views.accountSettings, name="account"),

    path('', views.home ,name="home"),
    path('product/', views.product, name="product"),
    path('customer/<int:pk>/', views.customer ,name="customer" ),
    path('createorder/',views.createorder, name="createorder"),
    path('updateorder/<int:pk>',views.updateorder, name="updateorder"),
    path('deleteorder/<int:pk>',views.deleteorder, name="deleteorder"),
]
