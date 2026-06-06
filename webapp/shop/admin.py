from django.contrib import admin
from django.utils.html import format_html
from .models import Coin, Banknote, Order, OrderItem, SliderBanner
from .utils import broadcast_message_to_all


# ---------------- SliderBanner Admin ----------------
@admin.register(SliderBanner)
class SliderBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'coin', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'coin__name')

    def image_preview(self, obj):
        return format_html('<img src="{}" width="100" />', obj.image.url)

    image_preview.short_description = "Прев'ю"


# ---------------- OrderItem Inline ----------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # Якщо ви змінили логіку в моделі на coin/banknote,
    # вкажіть відповідні поля тут
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


# ---------------- OrderAdmin ----------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'lastname', 'firstname', 'phone', 'delivery_service', 'city', 'created_at', 'sent_status')
    search_fields = ('lastname', 'firstname', 'phone', 'city')
    list_filter = ('delivery_service', 'city', 'created_at', 'sent')
    inlines = [OrderItemInline]

    # Тільки для читання - всі поля замовлення
    readonly_fields = ('created_at', 'lastname', 'firstname', 'phone', 'comment',
                       'city', 'np_office', 'ukr_office', 'delivery_service')

    def sent_status(self, obj):
        if obj.sent:
            return format_html('<span style="color: green; font-weight: bold;">✔ Відправлено</span>')
        return format_html('<span style="color: red;">❌ Не відправлено</span>')

    sent_status.short_description = "Статус відправки"


# ---------------- CoinAdmin ----------------
@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'price', 'material', 'category', 'is_new', 'is_ending')
    list_editable = ('is_new', 'is_ending')
    search_fields = ('name', 'year', 'material')
    list_filter = ('category', 'material', 'year', 'is_new', 'is_ending')

    def save_model(self, request, obj, form, change):
        is_new_coin = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new_coin:
            # Замініть на реальний домен
            msg = f"Новий товар: {obj.name} ({obj.year})\nДеталі: https://yourdomain.com/coin/{obj.id}/"
            broadcast_message_to_all(msg)


# ---------------- BanknoteAdmin ----------------
@admin.register(Banknote)
class BanknoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'price')
    search_fields = ('name', 'year')
    list_filter = ('year', 'category')