# Generated by Django 2.2.24 on 2021-08-08 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0023_auto_20210223_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='address',
            field=models.CharField(blank=True, max_length=150, verbose_name='Address'),
        ),
    ]
