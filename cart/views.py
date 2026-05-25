from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product


def _get_cart(request):
    return request.session.setdefault('cart', {})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)

    product_key = str(product.id)
    cart[product_key] = cart.get(product_key, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    product_key = str(product_id)

    if product_key in cart:
        cart[product_key] -= 1
        if cart[product_key] <= 0:
            del cart[product_key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def delete_from_cart(request, product_id):
    cart = _get_cart(request)
    product_key = str(product_id)

    if product_key in cart:
        del cart[product_key]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart_detail')


def cart_detail(request):
    cart = _get_cart(request)
    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })


def checkout(request):
    cart = _get_cart(request)

    if not cart:
        return redirect('cart_detail')

    cart_items = []
    total = Decimal('0.00')

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success')

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


def order_success(request):
    return render(request, 'cart/order_success.html')
