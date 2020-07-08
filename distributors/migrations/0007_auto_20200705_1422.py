# Generated by Django 3.0.6 on 2020-07-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0006_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='quantity',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='type',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]