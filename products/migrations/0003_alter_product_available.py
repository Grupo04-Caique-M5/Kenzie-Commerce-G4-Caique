# Generated by Django 4.2 on 2023-05-06 19:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="available",
            field=models.BooleanField(),
        ),
    ]