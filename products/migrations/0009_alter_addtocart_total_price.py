# Generated by Django 5.0.6 on 2024-06-05 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_addtocart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addtocart',
            name='total_price',
            field=models.FloatField(default=0),
        ),
    ]