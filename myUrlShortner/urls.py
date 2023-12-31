from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # if localhost:8000/hello
    # path('hello',views.hello_world),
    path('',views.home_page,name= "home"),
    # path('test', views.task)
    path('signup',views.sign_up,name = "signup"),
    path('signin',views.sign_in, name = "signin"),
    path('signout',views.sign_out, name = "signout"),
    # path('authHome',views.authHome,name="authHome"),
    path('all-analytics',views.all_analytics,name="urls"),
    path('<slug:DBreqCustomName>',views.redirect_url,name="db"),
#            ^       ^  
#            |       |
#         fixed    variable(any name can be given)
#           name       name
    path('activate/<uidb64>/<token>',views.activate, name = "activate"),

]