# Generated by Django 4.2 on 2023-05-04 18:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0003_address_delete_adress"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="address",
            name="user",
        ),
    ]