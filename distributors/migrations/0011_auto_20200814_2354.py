# Generated by Django 3.0.6 on 2020-08-14 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0010_auto_20200814_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='account_id',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
