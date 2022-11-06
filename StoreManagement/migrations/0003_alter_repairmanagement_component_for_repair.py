# Generated by Django 4.1.2 on 2022-11-06 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0002_alter_repairmanagement_component_for_repair'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairmanagement',
            name='component_for_repair',
            field=models.ForeignKey(limit_choices_to={'condition_received': '2'}, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.componentinstance', unique=True),
        ),
    ]
