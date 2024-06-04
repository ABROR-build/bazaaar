from django.db import models
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
    name = models.CharField(max_length=300)
    description = models.TextField()

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
    star_given = models.IntegerField()
    comment = models.TextField()

    class Meta:
        db_table = "Comments"

    def __str__(self):
        return f"comment of - {self.product.name}"
