from decimal import Decimal
from enum import unique
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Brand, Category, Product, ProductVariant, ProductImage, WishlistItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from .models import CartItem, Address, Order, OrderItem
from django.contrib.auth import update_session_auth_hash
import re


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


def personal_info_view(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    return render(request, 'ghost/personal_info.html', {
        'user': user,
        'addresses': addresses
    })


def add_address(request):
    is_default = request.POST.get('is_default') == 'on'

    if is_default:
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

    Address.objects.create(
        user=request.user,
        full_name=request.POST.get('full_name'),
        phone=request.POST.get('phone'),
        street=request.POST.get('street'),
        city=request.POST.get('city'),
        postal_code=request.POST.get('postal_code'),
        country=request.POST.get('country'),
        is_default=is_default
    )
    return redirect('personal_info')


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == "POST":
        address.full_name = request.POST.get('full_name')
        address.phone = request.POST.get('phone')
        address.street = request.POST.get('street')
        address.city = request.POST.get('city')
        address.postal_code = request.POST.get('postal_code')
        address.country = request.POST.get('country')

        if 'is_default' in request.POST:
            Address.objects.filter(user=request.user, is_default=True).exclude(id=address.id).update(is_default=False)
            address.is_default = True
        else:
            address.is_default = False

        address.save()
        return redirect('personal_info')

    return render(request, 'ghost/edit_address.html', {'address': address})


def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('personal_info')


def account_security(request):
    user = request.user
    errors = []

    old_password = user.password

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        if user.check_password(new_password):
            errors.append("Your new password must be different from the old one.")

        elif new_password != repeat_password:
            errors.append("Your passwords don't match.")

        elif len(new_password) < 8:
            errors.append("Your password must have at least 8 characters.")

        elif not re.search(r'\d', new_password):
            errors.append("Password must contain at least one digit.")

        elif not re.search(r'[A-Za-z]', new_password):
            errors.append("Password must contain at least one Latin letter.")

        elif not re.search(r'[!@#$%^&*,.?]', new_password):
            errors.append("Password must contain at least one special character.")

        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return render(request, 'ghost/account_security.html', {'success': True})

    return render(request, 'ghost/account_security.html', context={'errors': errors})


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
    wishlist_items_nike = WishlistItem.objects.filter(
        user=request.user,
        product__brand__name="Nike"
    ).select_related('product')

    wishlist_items_adidas = WishlistItem.objects.filter(
        user=request.user,
        product__brand__name="Adidas"
    ).select_related('product')

    wishlist_items_puma = WishlistItem.objects.filter(
        user=request.user,
        product__brand__name="Puma"
    ).select_related('product')

    wishlist_items = [wishlist_items_nike, wishlist_items_adidas, wishlist_items_puma]

    return render(request, 'ghost/wishlist.html', {'wishlist_items': wishlist_items})


def delete_item_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')


@login_required
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product_variant=variant,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product_variant__product')

    cart_items_nike = CartItem.objects.filter(
        user=request.user,
        product_variant__product__brand__name="Nike"
    ).select_related('product_variant__product')

    cart_items_adidas = CartItem.objects.filter(
        user=request.user,
        product_variant__product__brand__name="Adidas"
    ).select_related('product_variant__product')

    cart_items_puma = CartItem.objects.filter(
        user=request.user,
        product_variant__product__brand__name="Puma"
    ).select_related('product_variant__product')

    cart_item = [cart_items_nike, cart_items_adidas, cart_items_puma]
    total = sum([item.total_price() for item in cart_items])

    return render(request, 'ghost/cart.html', {
        'cart_items': cart_item,
        'total': total,
    })


@require_POST
def update_cart_quantity(request, item_id):
    new_quantity = int(request.POST.get('quantity', 1))
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if new_quantity > 0:
        item.quantity = new_quantity
        item.save()
    else:
        item.delete()

    return redirect('cart')


def delete_item_from_cart(request, item_id):
    CartItem.objects.filter(user=request.user, id=item_id).delete()
    return redirect('cart')


def checkout_single(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product = variant.product
    quantity = 1

    checkout_items = [{
        'product': product,
        'variant': variant,
        'quantity': quantity,
        'total_price': product.price
    }]

    checkout_items_session = [{
        'product_id': product.id,
        'variant_id': variant.id,
        'price': str(product.price),
        'quantity': 1
    }]

    request.session['checkout_items'] = checkout_items_session

    return render(request, 'ghost/checkout.html', {
        'checkout_items': checkout_items,
        'total_price': product.price,
        'discount': 0,
        'source': 'single',
        'shipping_methods': Order._meta.get_field('shipping_method').choices,
        'payment_methods': Order._meta.get_field('payment_method').choices,
    })

@require_POST
def checkout_selected(request):
    selected_ids = request.POST.getlist('selected_items')
    cart_items = CartItem.objects.filter(id__in=selected_ids, user=request.user)

    checkout_items = []
    checkout_items_session = []
    total_price = 0

    for item in cart_items:
        product = item.product_variant.product
        variant = item.product_variant
        quantity = item.quantity
        total = quantity * product.price

        checkout_items.append({
            'product': product,
            'variant': variant,
            'quantity': quantity,
            'total_price': total
        })
        checkout_items_session.append({
            'product_id': product.id,
            'variant_id': variant.id,
            'price': str(product.price),
            'quantity': quantity
        })

        total_price += total

    request.session['checkout_items'] = checkout_items_session

    return render(request, 'ghost/checkout.html', {
        'checkout_items': checkout_items,
        'total_price': total_price,
        'discount': 0,
        'source': 'cart',
        'shipping_methods': Order._meta.get_field('shipping_method').choices,
        'payment_methods': Order._meta.get_field('payment_method').choices,
    })


def checkout_all(request):
    cart_items = CartItem.objects.filter(user=request.user)

    checkout_items = []
    checkout_items_session = []
    total_price = 0

    for item in cart_items:
        product = item.product_variant.product
        variant = item.product_variant
        quantity = item.quantity
        total = quantity * product.price

        checkout_items.append({
            'product': product,
            'variant': variant,
            'quantity': quantity,
            'total_price': total
        })

        checkout_items_session.append({
            'product_id': product.id,
            'variant_id': variant.id,
            'price': str(product.price),
            'quantity': quantity
        })

        total_price += total

    request.session['checkout_items'] = checkout_items_session

    return render(request, 'ghost/checkout.html', {
        'checkout_items': checkout_items,
        'total_price': total_price,
        'discount': 0,
        'source': 'chart',
        'shipping_methods': Order._meta.get_field('shipping_method').choices,
        'payment_methods': Order._meta.get_field('payment_method').choices
    })



@require_POST
def place_order(request):
    address_id = request.POST.get('address_id')
    shipping = request.POST.get('shipping_method')
    payment = request.POST.get('payment_method')
    promo = request.POST.get('promo_code', '').strip()

    address = get_object_or_404(Address, id=address_id, user=request.user)
    raw_items = request.session.get('checkout_items', [])

    total_price = Decimal('0.00')
    parsed_items = []

    for entry in raw_items:
        product = get_object_or_404(Product, id=entry['product_id'])
        variant = get_object_or_404(ProductVariant, id=entry['variant_id'])
        price = Decimal(entry['price'])
        quantity = int(entry['quantity'])

        parsed_items.append((product, variant, price, quantity))
        total_price += price * quantity


    discount = 0
    if promo == 'asdf':
        discount = 10

    discount_amount = (total_price * Decimal(discount)) / Decimal('100')
    final_total = total_price - discount_amount

    order = Order.objects.create(
        user=request.user,
        address=address,
        shipping_method=shipping,
        payment_method=payment,
        promo_code=promo or None,
        discount=discount_amount,
        total_price=final_total,
        status='pending'
    )

    for product, variant, price, quantity in parsed_items:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )

    request.session['checkout_items'] = []

    return redirect('order_confirmation', order_id=order.id)


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ghost/order_history.html', {'orders': orders})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'ghost/order_confirmation.html', {
        'order': order
    })