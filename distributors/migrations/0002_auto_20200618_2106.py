# Generated by Django 3.0.6 on 2020-06-18 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributor',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='due',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='due',
            name='distributor',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='distributors.Distributor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='amount_paid',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='amount_paid',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='transaction_id',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='distributor',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/images/'),
        ),
    ]
