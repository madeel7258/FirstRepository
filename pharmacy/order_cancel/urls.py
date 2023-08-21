
from django.urls import path
from .views import *
from order_cancel import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('signup_data', views.signup_data, name='signup_data'),
    path('insert_data/', views.login, name='login'),
    path('show_order/', views.show_order, name='show_order'),
    path('logout', views.logout_view, name='logout'),
]
