from django.urls import path
from .views import product_list, cart_detail, cart_add, cart_remove

urlpatterns = [
    path('', product_list, name='product_list'),  # عرض قائمة المنتجات
    path('cart/', cart_detail, name='cart_detail'),  # عرض محتويات العربة
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),  # إضافة منتج
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),  # إزالة منتج
]
