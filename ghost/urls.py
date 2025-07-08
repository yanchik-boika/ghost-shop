from django.contrib import admin
from django.urls import path
from shop import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('nike/men/', views.nike_men, name='nike-men'),
    path('nike/women/', views.nike_women, name='nike-women'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)