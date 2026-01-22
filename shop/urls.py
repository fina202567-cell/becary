from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    # ======================
    # HOME
    # ======================
    path("", views.home, name="home"),

    # ======================
    # PRODUCTS
    # ======================
    path("products/", views.product_list, name="product_list"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # ======================
    # CART
    # ======================
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "cart/increase/<int:product_id>/",
        views.cart_increase,
        name="cart_increase"
    ),
    path(
        "cart/decrease/<int:product_id>/",
        views.cart_decrease,
        name="cart_decrease"
    ),

    # ======================
    # CHECKOUT & ORDERS
    # ======================
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.orders, name="orders"),
    path(
        "orders/<int:order_id>/",
        views.order_detail,
        name="order_detail"
    ),
]
