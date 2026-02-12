from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.shop_name

class Product(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ({self.quantity})"
    
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total price
        self.total_price = self.product.selling_price * self.quantity_sold
        # Deduct quantity from product
        self.product.quantity -= self.quantity_sold
        if self.product.quantity < 0:
            self.product.quantity = 0
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity_sold} x {self.product.name}"