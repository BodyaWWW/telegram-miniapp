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
    image = models.ImageField(upload_to="coins/")  # Главное фото
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="nbu_neizilber")
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    minting = models.CharField(max_length=255, null=True, blank=True)
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    edge = models.CharField(max_length=255, null=True, blank=True)
    circulation = models.IntegerField(null=True, blank=True)  # Тираж

    def __str__(self):
        return f"{self.name} ({self.year})"


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
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    np_office = models.CharField(max_length=255, blank=True, null=True)
    payment = models.CharField(max_length=50, blank=True, null=True)
    bank = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Coin', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class TelegramUser(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    joined = models.DateTimeField(auto_now_add=True)