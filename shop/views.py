from enum import unique
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Brand, Category, Product, ProductVariant, ProductImage, WishlistItem
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def home(request):
    return render(request, 'ghost/home.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'ghost/register.html', {'form': form})


from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'ghost/login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('home')




def filtered_products(request, brand, category):
    brand_obj = get_object_or_404(Brand, name__iexact=brand)
    category_obj = get_object_or_404(Category, slug__iexact=category)

    products = Product.objects.filter(brand=brand_obj, category=category_obj)

    products_filtered = []
    name_counts = {}

    for product in products:
        name = product.name
        count = name_counts.get(name, 0)

        if count < 3:
            products_filtered.append(product)
            name_counts[name] = count + 1


    context = {
        'brand': brand_obj,
        'category': category_obj,
        'products': products_filtered[:12]
    }
    return render(request, 'ghost/products.html', context)






def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    current_color = product.color

    images = ProductImage.objects.filter(product=product, color=current_color)

    family = Product.objects.filter(name=product.name, category=product.category).exclude(pk=product.pk)

    sizes = product.variants.values_list('size__label', flat=True).distinct()

    return render(request, 'ghost/product_detail.html', {
        'product': product,
        'images': images,
        'sizes': sizes,
        'product_family': family
    })


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def wishlist_view(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'ghost/wishlist.html', {'wishlist_items': wishlist_items})