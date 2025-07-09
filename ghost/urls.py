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

    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('<str:brand>/<str:category>/', views.filtered_products, name='filtered-products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)