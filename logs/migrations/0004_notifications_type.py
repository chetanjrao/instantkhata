# Generated by Django 3.0.6 on 2020-07-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='type',
            field=models.CharField(choices=[('B', 'Balance Notification'), ('I', 'Invoice Notification')], default='I', max_length=1),
            preserve_default=False,
        ),
    ]
