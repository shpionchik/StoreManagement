# Generated by Django 4.1.2 on 2022-11-18 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoreManagement', '0008_alter_componentinstance_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentinstance',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='media/certificate/%Y/%m/%d/'),
        ),
    ]
