# Generated by Django 2.2.24 on 2021-06-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chapters', '0005_auto_20210525_1232'),
    ]

    operations = [
        migrations.AddField(
            model_name='officer',
            name='expire_dt',
            field=models.DateField(blank=True, null=True, verbose_name='Expire Date'),
        ),
    ]
