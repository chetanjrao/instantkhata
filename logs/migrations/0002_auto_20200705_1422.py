# Generated by Django 3.0.6 on 2020-07-05 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='type',
            field=models.CharField(choices=[('A', 'ADDITION'), ('D', 'DELETION'), ('T', 'TRANSFER')], max_length=1),
        ),
    ]
