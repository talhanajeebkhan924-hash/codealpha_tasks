from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Product


@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(Product, pk=pk)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):

    items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price() for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total,
    })