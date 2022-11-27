# Generated by Django 4.1.2 on 2022-11-23 02:11

import django.contrib.auth.models
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0012_staff_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('StoreManagement.customuser',),
            managers=[
                ('viewer', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]