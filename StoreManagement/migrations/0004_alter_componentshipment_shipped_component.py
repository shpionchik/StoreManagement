# Generated by Django 4.1.2 on 2022-11-06 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0003_alter_repairmanagement_component_for_repair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentshipment',
            name='shipped_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.componentinstance', unique=True),
        ),
    ]
