# Generated by Django 3.0.6 on 2020-08-14 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0015_auto_20200815_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='distributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distributors.Distributor'),
        ),
    ]