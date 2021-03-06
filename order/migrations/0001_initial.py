# Generated by Django 3.2.9 on 2021-12-15 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('status', models.CharField(choices=[('pending', 'Pending'), ('scheduled', 'Scheduled'), ('delivered', 'Delivered'), ('failed', 'Delivery Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order_no', models.IntegerField(default=order.models.generate_order_no, editable=False, primary_key=True, serialize=False, unique=True)),
                ('unit', models.PositiveSmallIntegerField(default=1)),
                ('name', models.CharField(max_length=50)),
                ('billing_address', models.TextField()),
                ('time', models.TimeField(auto_now=True)),
                ('order_date', models.DateField(auto_now=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('updated', models.DateField(auto_now_add=True)),
                ('order', models.ForeignKey(max_length=100, on_delete=django.db.models.deletion.DO_NOTHING, to='main.food')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
    ]
