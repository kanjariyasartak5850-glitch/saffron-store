from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product, ProductVariant
from orders.models import Order, OrderItem
import json


def get_cart(request):
    """Get cart from session or create empty cart."""
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def save_cart(request, cart):
    """Save cart to session."""
    request.session['cart'] = cart
    request.session.modified = True


def product_list(request):
    """Display all active saffron products."""
    products = Product.objects.filter(is_active=True).prefetch_related('variants')
    context = {
        'products': products,
        'cart_count': len(get_cart(request)),
    }
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    """Display product details with variants."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.all()
    cart = get_cart(request)
    
    context = {
        'product': product,
        'variants': variants,
        'cart_count': len(cart),
    }
    return render(request, 'shop/product_detail.html', context)


@require_POST
def add_to_cart(request, variant_id):
    """Add product variant to cart."""
    variant = get_object_or_404(ProductVariant, id=variant_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart = get_cart(request)
    variant_id_str = str(variant_id)
    
    if variant_id_str in cart:
        cart[variant_id_str]['quantity'] += quantity
    else:
        cart[variant_id_str] = {
            'variant_id': variant_id,
            'product_name': variant.product.name,
            'weight_grams': variant.weight_grams,
            'price': str(variant.price),
            'quantity': quantity,
        }
    
    save_cart(request, cart)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'shop/cart_mini.html', {'cart_count': len(cart)})
    
    return redirect('shop:product_detail', slug=variant.product.slug)


def view_cart(request):
    """Display shopping cart."""
    cart = get_cart(request)
    cart_items = []
    total_amount = 0
    
    for variant_id_str, item in cart.items():
        variant = get_object_or_404(ProductVariant, id=item['variant_id'])
        item_total = float(item['price']) * item['quantity']
        total_amount += item_total
        cart_items.append({
            'variant': variant,
            'item': item,
            'total': item_total,
        })
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_count': len(cart),
    }
    return render(request, 'shop/cart.html', context)


@require_POST
def remove_from_cart(request, variant_id):
    """Remove item from cart."""
    cart = get_cart(request)
    variant_id_str = str(variant_id)
    
    if variant_id_str in cart:
        del cart[variant_id_str]
    
    save_cart(request, cart)
    return redirect('shop:view_cart')


@require_POST
def update_cart(request, variant_id):
    """Update quantity of cart item."""
    cart = get_cart(request)
    variant_id_str = str(variant_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if variant_id_str in cart:
        if quantity <= 0:
            del cart[variant_id_str]
        else:
            cart[variant_id_str]['quantity'] = quantity
    
    save_cart(request, cart)
    return redirect('shop:view_cart')


def checkout(request):
    """Checkout view - display order form."""
    cart = get_cart(request)
    
    if not cart:
        return redirect('shop:product_list')
    
    cart_items = []
    total_amount = 0
    
    for variant_id_str, item in cart.items():
        variant = get_object_or_404(ProductVariant, id=item['variant_id'])
        item_total = float(item['price']) * item['quantity']
        total_amount += item_total
        cart_items.append({
            'variant': variant,
            'item': item,
            'total': item_total,
        })
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'cart_count': len(cart),
    }
    return render(request, 'shop/checkout.html', context)


def order_success(request, order_id):
    """Display order success page."""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'shop/order_success.html', context)
