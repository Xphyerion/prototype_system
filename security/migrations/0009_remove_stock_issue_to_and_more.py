# Generated by Django 4.1.7 on 2023-04-18 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0008_remove_stock_low_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='issue_to',
        ),
        migrations.RemoveField(
            model_name='stock_history_log',
            name='issue_to',
        ),
    ]
