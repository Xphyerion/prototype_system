# Generated by Django 4.1.7 on 2023-04-17 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0005_remove_stock_is_active_remove_stock_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='updated_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='stock_history_log',
            name='updated_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
