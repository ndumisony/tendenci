# Generated by Django 3.2.16 on 2023-04-24 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0004_auto_20220228_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='enforce_direct_mail_flag',
            field=models.BooleanField(default=True, verbose_name="Skip members that have opted for Don't Send Email in their profile"),
        ),
    ]
