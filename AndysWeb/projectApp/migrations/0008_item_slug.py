# Generated by Django 4.0.1 on 2022-06-15 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectApp', '0007_item_category_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test-product'),
            preserve_default=False,
        ),
    ]
