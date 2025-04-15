from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.cartPage , name='cartPage'),
    path('add-cart/', views.cartAdd , name='cart_add'),
    path('cart-update/', views.cartUpdate , name='cart_update'),
    path('cartItem-delete/', views.cartDelete , name='cart_delete'),
    path('order-placed/',views.orderPlace , name='orderPlace'),

] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
