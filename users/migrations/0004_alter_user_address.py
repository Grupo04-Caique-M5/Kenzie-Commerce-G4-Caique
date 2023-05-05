# Generated by Django 4.2 on 2023-05-05 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("addresses", "0004_remove_address_user"),
        ("users", "0003_alter_user_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to="addresses.address",
            ),
        ),
    ]