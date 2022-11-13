# Generated by Django 4.1.2 on 2022-11-13 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='componentshipment',
            name='shipped_quantity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='componentshipment',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.quantitytype'),
        ),
    ]