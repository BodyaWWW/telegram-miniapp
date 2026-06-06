from django.db import models


class Coin(models.Model):
    CATEGORY_CHOICES = [
        ("nbu_neizilber", "Монети НБУ з нейзильберу"),
        ("nbu_silver", "Срібні монети НБУ"),
        ("ancient", "Старовинні монети"),
        ("investment", "Інвестиційні монети країн Світу"),
    ]

    name = models.CharField(max_length=255)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=50)
    image = models.ImageField(upload_to="coins/")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="nbu_neizilber")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minting = models.CharField(max_length=255, null=True, blank=True)
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    edge = models.CharField(max_length=255, null=True, blank=True)
    circulation = models.IntegerField(null=True, blank=True)

    # Нові поля для тегів
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    is_ending = models.BooleanField(default=False, verbose_name="Закінчується")

    def __str__(self):
        return f"{self.name} ({self.year})"


class SliderBanner(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок банера")
    image = models.ImageField(upload_to="banners/", verbose_name="Фото банера")
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="banners")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок показу")
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    class Meta:
        ordering = ['order']
        verbose_name = "Банер"
        verbose_name_plural = "Банери (Слайдер)"

    def __str__(self):
        return self.title


class CoinImage(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="coins/multiple/")

    def __str__(self):
        return f"Доп. изображение для {self.coin.name}"

class Banknote(models.Model):
    CATEGORY_CHOICES = [
        ("nbu", "Банкноти НБУ"),
        ("world", "Банкноти Країн Світу"),
    ]


    name = models.CharField(max_length=200)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='coins/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="nbu")

    def __str__(self):
        return f"{self.name} ({self.year})"


class Order(models.Model):
    # Додаємо прізвище та ім'я окремо, як у формі
    lastname = models.CharField(max_length=255, verbose_name="Прізвище", null=True, blank=True)
    firstname = models.CharField(max_length=255, verbose_name="Ім'я", null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Коментар")

    # Дані доставки
    delivery_service = models.CharField(max_length=50, verbose_name="Служба доставки", null=True, blank=True)  # 'nova' або 'ukr'
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Місто")
    np_office = models.CharField(max_length=255, blank=True, null=True, verbose_name="Відділення НП")
    ukr_office = models.CharField(max_length=255, blank=True, null=True, verbose_name="Відділення Укрпошти")

    # Інші поля
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False, verbose_name="Відправлено")
    telegram_user_id = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', verbose_name="Статус")

    def __str__(self):
        return f"Замовлення {self.id} - {self.lastname} {self.firstname}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Coin', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    joined = models.DateTimeField(auto_now_add=True)