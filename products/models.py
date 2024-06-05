from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.name


class Pages(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Pages'

    def __str__(self):
        return self.name


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    page = models.ForeignKey(Pages, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.TextField()

    price = models.FloatField()

    discount = models.IntegerField(default=0)
    price_discount = models.IntegerField(default=1)

    def calculate_price_discount(self):
        return self.price - ((self.price // 100) * self.discount)

    def save(self, *args, **kwargs):
        self.price_discount = self.calculate_price_discount()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.name


class Images(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = 'Images'

    def __str__(self):
        return f"image of - {self.product.name}"


class Comments(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Comments"

    def __str__(self):
        return f"comment of - {self.product.name}"
