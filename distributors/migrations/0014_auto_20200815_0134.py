# Generated by Django 3.0.6 on 2020-08-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0013_auto_20200815_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='payment_id',
            field=models.CharField(default=None, max_length=512),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='due',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='duration',
            field=models.IntegerField(help_text='Total days this packages will work'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='created_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='payment_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
