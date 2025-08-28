from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order/<int:order_id>/checkout/", views.create_checkout_session, name="checkout"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
]
