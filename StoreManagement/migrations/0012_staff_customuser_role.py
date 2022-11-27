# Generated by Django 4.1.2 on 2022-11-22 19:16

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0011_shelf_alter_component_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('StoreManagement.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('STAFF', 'Staff'), ('VIEWER', 'Viewer')], default=1, max_length=50),
            preserve_default=False,
        ),
    ]