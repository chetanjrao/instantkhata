# Generated by Django 3.0.6 on 2020-07-16 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_otp_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/profile/'),
        ),
    ]
