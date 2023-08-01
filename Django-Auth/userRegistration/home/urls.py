
from django.urls import path
from django.urls import path
from home import views #correct this redline warning
'''
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
'''
urlpatterns = [
    path("", views.user_signup,name='user_signup'),
    path('home_page', views.home_page, name='home_page'),
    path("user_login",views.user_login,name='user_login'),
    path('user_signup', views.user_signup, name='user_signup'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('api_user_login', views.api_user_login, name='api_user_login'),
    path('view_users_api', views.view_users_api, name='view_users_api'),

]

