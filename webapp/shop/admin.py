from django.contrib import admin
from django.utils.html import format_html
from .models import Coin, Banknote, Order, OrderItem
from .utils import broadcast_message_to_all

from django.contrib import admin
from django.utils.html import format_html
from .models import Coin, Banknote, Order, OrderItem
from .utils import broadcast_message_to_all

# ---------------- OrderItem Inline ----------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False

# ---------------- OrderAdmin ----------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'city', 'np_office', 'payment', 'created_at', 'sent_status')
    search_fields = ('name', 'phone')
    list_filter = ('payment', 'city', 'created_at', 'sent')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'name', 'phone', 'comment', 'city', 'np_office', 'payment', 'bank')

    # Статус отправки — подсветка строки
    def sent_status(self, obj):
        if obj.sent:  # предполагаем, что в модели есть BooleanField sent=True если отправлен
            return format_html('<span style="background-color: #FFEB3B; padding:2px 5px; border-radius:3px;">Отправлено</span>')
        return "Не отправлено"
    sent_status.short_description = "Статус отправки"

    # Цвет строк таблицы — если отправлено
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def changelist_view(self, request, extra_context=None):
        # Можно добавить кастомный JS/CSS если нужно менять цвет строк — позже
        return super().changelist_view(request, extra_context=extra_context)

# ---------------- CoinAdmin ----------------
@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'price', 'material', 'category')
    search_fields = ('name', 'year', 'material')
    list_filter = ('category', 'material', 'year')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            msg = f"Новий товар: {obj.name} ({obj.year})\nДеталі: https://твой-сайт/coin/{obj.id}/"
            broadcast_message_to_all(msg)

# ---------------- BanknoteAdmin ----------------
@admin.register(Banknote)
class BanknoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'price')
    search_fields = ('name', 'year')
    list_filter = ('year',)

