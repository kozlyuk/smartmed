# Generated by Django 2.2.3 on 2019-07-29 17:22

import catalogue.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Attribute')),
            ],
            options={
                'verbose_name': 'Attribute type',
                'verbose_name_plural': 'Attribute types',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=45, verbose_name='Attribute Value')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Brand name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Brand Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Category name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Brand Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Group name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='groups/', verbose_name='Brand Image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=catalogue.models.image_directory_path, verbose_name='Product image')),
                ('main', models.BooleanField(default=True, verbose_name='Is main image')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='PriceRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default=django.utils.timezone.now, verbose_name='Actual from')),
                ('regular_price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Product price')),
                ('discount_price_1', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Discount price')),
                ('discount_price_2', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Discount price')),
                ('discount_price_3', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Discount price')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Created')),
                ('date_updated', models.DateField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Price Record',
                'verbose_name_plural': 'Price Records',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Product title')),
                ('upc', models.CharField(max_length=32, unique=True, verbose_name='Product UPC')),
                ('description', models.TextField(blank=True, verbose_name='Product description')),
                ('warranty_terms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Warranty terms, months')),
                ('default_uom', models.CharField(default='pcs.', max_length=8, verbose_name='Default units of measurement')),
                ('pack_size', models.PositiveSmallIntegerField(default=10, verbose_name='Pack size')),
                ('min_store_quantity', models.IntegerField(default=10, verbose_name='Minimal store quantity')),
                ('has_instances', models.BooleanField(default=True, verbose_name='Has instances')),
                ('is_discountable', models.BooleanField(default=True, verbose_name='Discountable')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Created')),
                ('date_updated', models.DateField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-date_created', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_name', models.CharField(blank=True, max_length=64, verbose_name='Instance name')),
                ('serial_number', models.CharField(max_length=32, unique=True, verbose_name='Serial Number')),
                ('warranty_end_date', models.DateField(verbose_name='Warranty end date')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Created')),
                ('date_updated', models.DateField(auto_now=True, verbose_name='Updated')),
                ('attribute_values', models.ManyToManyField(blank=True, to='catalogue.AttributeValue', verbose_name='Attributes')),
                ('created_by', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'Product Instance',
                'verbose_name_plural': 'Product Instances',
            },
        ),
    ]
