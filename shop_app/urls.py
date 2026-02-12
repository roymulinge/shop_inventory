from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LogoutGetAllowedView 
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('daily-summary/', views.daily_summary, name='daily_summary'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutGetAllowedView.as_view(next_page='/accounts/login/'), name='logout'),
    path('login/', auth_views.LoginView.as_view, name='login'),
    
]