from django.urls import path
from . import views

urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('new-announcements/', views.new_announcements, name='new_announcements'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
] 