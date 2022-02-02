# Generated by Django 3.2 on 2022-02-02 23:06

import builtins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0026_orderbox_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbox',
            name='customer',
            field=models.ForeignKey(default=builtins.id, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
