# Generated by Django 3.0.6 on 2020-08-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retailers', '0003_auto_20200716_2248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('mobile', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
    ]
