# Generated by Django 4.1.6 on 2023-02-15 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(default='1', max_length=10),
            preserve_default=False,
        ),
    ]
