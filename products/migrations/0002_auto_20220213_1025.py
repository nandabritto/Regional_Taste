# Generated by Django 3.2 on 2022-02-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_note1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_note2',
            field=models.TextField(blank=True, null=True),
        ),
    ]
