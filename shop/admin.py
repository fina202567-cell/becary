from django.contrib import admin
from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    ContactMessage,
)

# ======================
# CATEGORY
# ======================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ======================
# PRODUCT
# ======================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "created_at")
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("-created_at",)


# ======================
# CART (OPTIONAL VIEW)
# ======================
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product", "quantity")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    inlines = [CartItemInline]
    readonly_fields = ("user", "created_at", "updated_at")


# ======================
# ORDER (🔥 IMPORTANT 🔥)
# ======================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "id")
    ordering = ("-created_at",)

    readonly_fields = (
        "user",
        "subtotal",
        "tax",
        "total_price",
        "created_at",
    )

    inlines = [OrderItemInline]

    fieldsets = (
        ("Customer", {
            "fields": ("user",),
        }),
        ("Payment", {
            "fields": ("subtotal", "tax", "total_price"),
        }),
        ("Order Status", {
            "fields": ("status",),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )


# ======================
# CONTACT MESSAGES
# ======================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    readonly_fields = ("name", "email", "message", "created_at")
