from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from shop import views
from django.conf import settings
from django.conf.urls.static import static

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('account/', views.personal_info_view, name='personal_info'),
    path('account/add-address/', views.add_address, name='add_address'),

    path('account/edit-address/<int:address_id>', views.edit_address, name='edit_address'),
    path('account/delete-address/<int:address_id>', views.delete_address, name='delete_address'),

    path('account/security', views.account_security, name='account_security'),

    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/delete/<int:product_id>/', views.delete_item_from_wishlist, name='delete_item_from_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),

    path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/delete/<int:item_id>/', views.delete_item_from_cart, name='delete_item_from_cart'),
    path('cart/', views.cart_view, name='cart'),

    path('<str:brand>/<str:category>/', views.filtered_products, name='filtered-products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)