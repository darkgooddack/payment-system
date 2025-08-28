import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Order, Product, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    products = Product.objects.all()
    orders = Order.objects.all().order_by("-id")  # последние сверху
    return render(request, "payments/index.html", {
        "products": products,
        "orders": orders,
    })


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "payments/order_detail.html", {
        "order": order,
        "stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    line_items = []
    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": item.product.name},
                "unit_amount": item.product.price,
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
    )
    order.is_paid = True
    order.save()

    return JsonResponse({"id": session.id})


def success(request):
    return render(request, "payments/payment_status.html", {"paid": True})

def cancel(request):
    return render(request, "payments/payment_status.html", {"paid": False})
