# Generated by Django 3.2 on 2022-02-02 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0028_alter_orderbox_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_profile',
        ),
        migrations.RemoveField(
            model_name='orderbox',
            name='customer',
        ),
    ]