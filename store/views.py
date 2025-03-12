from django.shortcuts import redirect, get_object_or_404, render
from .models import Product
from .cart import Cart

# عرض قائمة المنتجات وإضافة منتج للعربة
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/cart_view.html', {'products': products})

# عرض محتويات العربة
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart_detail.html', {'cart': cart})

# إضافة منتج إلى العربة
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart_detail')

# إزالة منتج من العربة
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')
