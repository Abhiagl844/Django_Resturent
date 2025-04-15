from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home , name='home'),
    path('login/', views.loginPage , name='login'),
    path('logout/',views.logoutPage , name='logout'),
    path('register/',views.registerPage, name='register'),
    path('userRegister/',views.user_deltail_Form , name='user_details_form'),
    path('dashboard/',views.dashPage , name='dashboard'),

    path('food/<str:pk>',views.foodPage , name='foodPage'),

    path('menuCreate/',views.menuCreation , name='create-menu'),
    path('menuUpdate/<str:pk>',views.menuUpdation , name='update-menu'),
    path('menuDelete/<str:pk>',views.menuDeletion , name='delete-menu'),

    path('user_update',views.user_deltail_Form , name='user-update'),
    path('orders',views.user_orders , name='user-order'),


] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
