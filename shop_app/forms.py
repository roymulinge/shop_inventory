# shop_app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Product, SellerProfile
from django.contrib.auth.forms import UserCreationForm

class SellerRegistrationForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'shop_name', 'phone_number']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'selling_price', 'buying_price']