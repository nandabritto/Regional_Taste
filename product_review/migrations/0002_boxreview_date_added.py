# Generated by Django 3.2 on 2022-02-06 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product_review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxreview',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]