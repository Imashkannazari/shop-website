from django.shortcuts import render, get_object_or_404
from home.models import Product
from django.http import JsonResponse
from django.urls import reverse
from .models import CartItem
# Create your views here.
def cart_summary(request):
    if not request.user.is_authenticated:
        return render(request, 'cart_summary.html', {'cart_items': [], 'total_price': 0})

    cart_items_qs = CartItem.objects.filter(user=request.user).select_related('product')
    cart_items = []
    total_price = 0
    for item in cart_items_qs:
        line_total = item.product.price * item.quantity
        total_price += line_total
        cart_items.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': item.product.price,
            'line_total': line_total,
        })
    return render(request, 'cart_summary.html', {'cart_items': cart_items, 'total_price': total_price})


def cart_add(request):
    if request.POST.get('action') != 'post':
        return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'auth_required',
            'message': 'برای افزودن محصول باید ثبت نام یا ورود انجام دهید.',
            'redirect_url': reverse('singup'),
        }, status=401)

    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity', 'updated_at'])

    cart_count = CartItem.objects.filter(user=request.user).count()
    return JsonResponse({
        'status': 'ok',
        'message': 'محصول به سبد خرید اضافه شد.',
        'product_name': product.name,
        'cart_count': cart_count,
    })


def cart_delete(request):
    pass


def cart_update(request):
    pass