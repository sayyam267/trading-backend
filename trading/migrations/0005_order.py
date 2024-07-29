# Generated by Django 5.0.1 on 2024-03-18 14:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0004_alter_credential_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('Market', 'market')], max_length=10)),
                ('order_action', models.CharField(choices=[('Buy', 'buy'), ('Sell', 'sell')], max_length=10)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('FILLED', 'Filled'), ('PARTIALLY_FILLED', 'Partially Filled'), ('CANCELLED', 'Cancelled')], max_length=16)),
                ('platform_type', models.CharField(choices=[('binance', 'Binance'), ('oanda', 'Oanda'), ('alpace', 'Alpace')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]