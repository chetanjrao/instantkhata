# Generated by Django 3.0.6 on 2020-07-07 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0007_auto_20200705_1422'),
        ('ledger', '0003_auto_20200706_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='distributor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='distributors.Distributor'),
            preserve_default=False,
        ),
    ]
