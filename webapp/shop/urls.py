from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import index, api_create_order,coin_detail

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
    path('favorites/', views.favorites, name='favorites'),
    path('cart/', views.cart_view, name='cart'),
    path('api/create_order/', api_create_order, name='api_create_order'),
    path('np_proxy/', views.np_proxy, name='np_proxy'),
    path('coin/<int:pk>/', views.coin_detail, name='coin_detail'),
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:slug>/', views.category_detail, name='category_detail'),
    path('ajax/search_coins/', views.ajax_search_coins, name='ajax_search_coins'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
