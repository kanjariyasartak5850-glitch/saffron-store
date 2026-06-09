from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from shop.models import ProductVariant
from .models import Order, OrderItem


def get_cart(request):
    """Get cart from session."""
    return request.session.get('cart', {})


@require_POST
def create_order(request):
    """Create an order and prepare for Razorpay payment."""
    cart = get_cart(request)
    
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('shop:product_list')
    
    # Get form data
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    pincode = request.POST.get('pincode', '').strip()
    
    # Validate required fields
    if not all([full_name, email, phone, address, city, state, pincode]):
        messages.error(request, 'Please fill in all fields!')
        return redirect('shop:checkout')
    
    # Calculate total amount
    total_amount = 0
    order_items_data = []
    
    for variant_id_str, item in cart.items():
        try:
            variant = ProductVariant.objects.get(id=item['variant_id'])
            item_total = float(item['price']) * item['quantity']
            total_amount += item_total
            
            order_items_data.append({
                'variant': variant,
                'quantity': item['quantity'],
                'price': float(item['price']),
            })
        except ProductVariant.DoesNotExist:
            messages.error(request, 'Product variant not found!')
            return redirect('shop:view_cart')
    
    if not order_items_data:
        messages.error(request, 'Your cart is empty!')
        return redirect('shop:product_list')
    
    # Create Order with pending status
    try:
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total_amount,
            status='pending',
        )
        
        # Create OrderItems
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                variant=item_data['variant'],
                quantity=item_data['quantity'],
                price=item_data['price'],
            )
        
        # Create Razorpay order
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Amount in paise (₹1 = 100 paise)
        razorpay_order = client.order.create(
            {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': 1,  # Auto capture payment
            }
        )
        
        # Save Razorpay order ID
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        # Render payment page with Razorpay details
        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': int(total_amount * 100),
            'order_items': order.items.all(),
            'DEBUG': settings.DEBUG,
        }
        
        return render(request, 'shop/payment.html', context)
        
    except Exception as e:
        messages.error(request, f'Error creating order: {str(e)}')
        return redirect('shop:checkout')


@csrf_exempt
@require_http_methods(['POST'])
def verify_payment(request):
    """Verify Razorpay payment and update order status."""
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        print(f"[DEBUG] Verifying payment: {razorpay_order_id}, {razorpay_payment_id}")
        
        # Get order
        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            print(f"[ERROR] Order not found for {razorpay_order_id}")
            return JsonResponse({
                'success': False,
                'message': f'Order not found',
            }, status=400)
        
        # In test mode, allow test payments to bypass signature verification
        is_test_payment = razorpay_payment_id == 'test_payment_id' and razorpay_signature == 'test_signature'
        
        if not is_test_payment:
            # Verify payment signature for real payments
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            
            verify_data = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            }
            
            try:
                # Verify signature
                client.utility.verify_payment_signature(verify_data)
                print(f"[SUCCESS] Payment signature verified for {razorpay_order_id}")
            except razorpay.errors.SignatureVerificationError as e:
                print(f"[ERROR] Signature verification failed: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'message': 'Payment signature verification failed',
                }, status=400)
        else:
            print(f"[TEST MODE] Accepting test payment for {razorpay_order_id}")
        
        # Payment verified - update order
        order.razorpay_payment_id = razorpay_payment_id
        order.status = 'paid'
        order.save()
        print(f"[SUCCESS] Order {order.id} status updated to 'paid'")
        
        # Clear session cart
        request.session['cart'] = {}
        request.session.modified = True
        
        return JsonResponse({
            'success': True,
            'message': 'Payment verified successfully',
            'order_id': order.id,
        })
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format',
        }, status=400)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}',
        }, status=500)


def payment_success(request, order_id):
    """Payment success page."""
    order = get_object_or_404(Order, id=order_id, status='paid')
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'shop/order_success.html', context)


def payment_failed(request, order_id):
    """Payment failed page."""
    order = get_object_or_404(Order, id=order_id, status='pending')
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('shop:checkout')
