from django.contrib import admin
from .models import Coin, Banknote, Order, OrderItem,TelegramUser
from .utils import broadcast_message_to_all  # Импортируй функцию рассылки

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'city', 'np_office', 'payment', 'created_at')
    search_fields = ('name', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'name', 'phone', 'comment', 'city', 'np_office', 'payment', 'bank')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    search_fields = ('order__name', 'product__name')


# Вот тут важная часть!
@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'price', 'material', 'category')
    search_fields = ('name', 'year', 'material')

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None
        super().save_model(request, obj, form, change)
        if is_new:
            print("Создана новая монета! Рассылка пошла...")  # <-- Должно появиться в логах
            msg = f"Новий товар: {obj.name} ({obj.year})\nДеталі: https://твой-сайт/coin/{obj.id}/"
            broadcast_message_to_all(msg)

admin.site.register(Banknote)
admin.site.register(TelegramUser)