# Generated by Django 3.0.6 on 2020-07-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0007_auto_20200705_1422'),
        ('salesman', '0002_auto_20200705_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesman',
            name='distributor',
            field=models.ManyToManyField(blank=True, to='distributors.Distributor'),
        ),
    ]