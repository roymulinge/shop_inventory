from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, SellerProfile
from .forms import ProductForm, SellerRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView

class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
def register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create SellerProfile for this user
            shop_name = form.cleaned_data.get('shop_name')
            phone_number = form.cleaned_data.get('phone_number')
            user.sellerprofile = SellerProfile.objects.create(
                user=user, shop_name=shop_name, phone_number=phone_number
            )
            login(request, user)  # log the user in immediately
            messages.success(request, 'Registration successful!')
            return redirect('product_list')
    else:
        form = SellerRegistrationForm()
    return render(request, 'shop_app/register.html', {'form': form})

@login_required
def product_list(request):
    # Show only products for the logged-in seller
    products = Product.objects.filter(seller=request.user.sellerprofile)
    return render(request, 'shop_app/product_list.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.sellerprofile  # link to seller
            product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'shop_app/product_add.html', {'form': form})

@login_required
def edit_product(request, id):
    # Only allow editing of products belonging to this seller
    product = get_object_or_404(Product, id=id, seller=request.user.sellerprofile)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop_app/product_add.html', {'form': form})

@login_required
def delete_product(request, id):
    # Only allow deletion of products belonging to this seller
    product = get_object_or_404(Product, id=id, seller=request.user.sellerprofile)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('product_list')

@login_required
def daily_summary(request):
    # Only show daily summary for the logged-in seller
    products = Product.objects.filter(seller=request.user.sellerprofile)
    total_qty = sum([p.quantity for p in products])
    total_value = sum([p.quantity * p.selling_price for p in products])
    return render(request, 'shop_app/daily_summary.html', {
        'total_qty': total_qty,
        'total_value': total_value,
        'products': products
    })