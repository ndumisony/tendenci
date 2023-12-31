# Generated by Django 3.2.12 on 2022-11-24 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20200902_1545'),
        ('committees', '0008_officer_expire_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='featured_image',
            field=models.ForeignKey(default=None, help_text='Only jpg, gif, or png images.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='committees', to='files.file'),
        ),
    ]
