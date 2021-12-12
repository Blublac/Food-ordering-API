# Generated by Django 3.2.9 on 2021-12-11 08:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_category_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('subcategory', models.CharField(default=(('Bakery', ('cake', 'cookies', 'bread', 'pies', 'pizza')), ('rice', ('jollof rice', 'fried rice', 'chinese rice', 'rice & stew', 'coconut rice')), ('roast', ('corn', 'beans & roasted plantain', 'bole', 'roasted chicken')), ('barbeque', ('grilled chicken', 'grilled beef', 'grilled fish', 'suya')), ('sharwarma', ('chicken', 'beef', 'chicken jumbo+2hotdog', 'beef jumbo+2hotdog'))), max_length=100)),
                ('details', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('sku_no', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('food', models.CharField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categorie')),
            ],
        ),
        migrations.RemoveField(
            model_name='foods',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Foods',
        ),
    ]