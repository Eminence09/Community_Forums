from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] 