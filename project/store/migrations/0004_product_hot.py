# Generated by Django 5.0.6 on 2024-07-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hot',
            field=models.BooleanField(default=False),
        ),
    ]
