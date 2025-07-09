from django.contrib import admin
from .models import (
    Brand, Category, Product, ProductImage,
    Size, Color, ProductVariant,
    Order, WishlistItem
)

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(ProductVariant)
admin.site.register(Order)
admin.site.register(WishlistItem)

