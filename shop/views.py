from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Cart, CartItem, Order, OrderItem

TAX_RATE = Decimal("0.10")  # 10% tax


# ======================
# HOME
# ======================
def home(request):
    products = Product.objects.select_related("category")
    categories = Category.objects.all()

    return render(request, "shop/home.html", {
        "products": products,
        "categories": categories,
    })


# ======================
# PRODUCT LIST
# ======================
def product_list(request):
    category_id = request.GET.get("category")

    products = Product.objects.select_related("category")
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, "shop/products.html", {
        "products": products,
        "categories": categories,
        "selected_category": category_id,
    })


# ======================
# PRODUCT DETAIL
# ======================
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {
        "product": product
    })


# ======================
# ADD TO CART
# ======================
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(request, f"{product.name} added to cart 🛒")
    return redirect("shop:cart")


# ======================
# CART
# ======================
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product")

    display_items = []

    for item in cart_items:
        tax = (item.product.price * TAX_RATE).quantize(Decimal("0.01"))
        price_incl_tax = item.product.price + tax
        subtotal_incl_tax = (price_incl_tax * item.quantity).quantize(Decimal("0.01"))

        display_items.append({
            "item": item,
            "tax": tax,
            "price_incl_tax": price_incl_tax,
            "subtotal": subtotal_incl_tax,
        })

    return render(request, "shop/cart.html", {
        "cart_items": display_items,
        "subtotal": cart.subtotal,
        "tax_total": cart.tax,
        "total": cart.total,
        "tax_rate": int(TAX_RATE * 100),
    })


# ======================
# CART + / −
# ======================
@login_required
def cart_increase(request, product_id):
    cart = request.user.cart
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.quantity += 1
    item.save()
    return redirect("shop:cart")


@login_required
def cart_decrease(request, product_id):
    cart = request.user.cart
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("shop:cart")


# ======================
# REMOVE FROM CART
# ======================
@login_required
def remove_from_cart(request, product_id):
    cart = request.user.cart
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    messages.info(request, "Item removed from cart")
    return redirect("shop:cart")


# ======================
# CHECKOUT
# ======================
@login_required
def checkout(request):
    cart = request.user.cart
    cart_items = cart.items.select_related("product")

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty 😅")
        return redirect("shop:product_list")

    display_items = []

    for item in cart_items:
        tax = (item.product.price * TAX_RATE).quantize(Decimal("0.01"))
        price_incl_tax = item.product.price + tax
        subtotal_incl_tax = (price_incl_tax * item.quantity).quantize(Decimal("0.01"))

        display_items.append({
            "item": item,
            "tax": tax,
            "price_incl_tax": price_incl_tax,
            "subtotal": subtotal_incl_tax,
        })

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            subtotal=cart.subtotal,
            tax=cart.tax,
            total_price=cart.total,
            status="paid"
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        cart_items.delete()
        messages.success(request, "Order placed successfully 🎉")
        return redirect("shop:order_detail", order_id=order.id)

    return render(request, "shop/checkout.html", {
        "items": display_items,
        "subtotal": cart.subtotal,
        "tax_total": cart.tax,
        "total": cart.total,
        "tax_rate": int(TAX_RATE * 100),
    })


# ======================
# ORDER HISTORY
# ======================
@login_required
def orders(request):
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )

    return render(request, "shop/orders.html", {
        "orders": orders
    })


# ======================
# ORDER DETAIL
# ======================
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user
    )

    return render(request, "shop/order_detail.html", {
        "order": order
    })
