# Generated by Django 5.1.1 on 2024-11-06 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart_item',
            old_name='product',
            new_name='Product',
        ),
    ]
