# Generated by Django 4.1.2 on 2022-11-04 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentinstance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
