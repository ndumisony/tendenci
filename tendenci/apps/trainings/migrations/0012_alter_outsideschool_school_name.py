# Generated by Django 3.2.16 on 2023-03-02 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0011_auto_20230302_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outsideschool',
            name='school_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
