# Generated by Django 3.2 on 2022-02-19 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_alter_newsletter_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='status',
        ),
        migrations.RemoveField(
            model_name='newsletter',
            name='updated',
        ),
    ]
