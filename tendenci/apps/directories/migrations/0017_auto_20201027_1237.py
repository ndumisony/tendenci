# Generated by Django 2.2.16 on 2020-10-27 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0016_auto_20201010_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('position', 'name'), 'verbose_name_plural': 'Categories'},
        ),
    ]
