# Generated by Django 5.0.6 on 2024-07-04 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='gender',
        ),
    ]