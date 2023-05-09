# Generated by Django 4.2 on 2023-05-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(related_name='carts', to='products.product'),
        ),
    ]
