# Generated by Django 4.1.2 on 2022-11-12 20:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('part_number', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'ComponentAbstract',
                'verbose_name_plural': 'ComponentsAbstract',
            },
        ),
        migrations.CreateModel(
            name='ComponentInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=50)),
                ('date_received', models.DateField(default=django.utils.timezone.now)),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('received_from', models.CharField(max_length=30)),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('certificate_number', models.CharField(blank=True, max_length=50, null=True)),
                ('shelf_life', models.CharField(blank=True, max_length=50, null=True)),
                ('us_part_condition', models.CharField(blank=True, max_length=50, null=True)),
                ('notes', models.CharField(blank=True, max_length=50, null=True)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='certificate/')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.component')),
            ],
            options={
                'verbose_name': 'Component',
                'verbose_name_plural': 'Components',
                'ordering': ('component',),
            },
        ),
        migrations.CreateModel(
            name='ComponentShipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shipped', models.DateField(default=django.utils.timezone.now)),
                ('shipped_to', models.CharField(blank=True, max_length=30, null=True)),
                ('invoice', models.CharField(blank=True, max_length=30, null=True)),
                ('shipping_order_notes', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Condition',
                'verbose_name_plural': 'Conditions',
                'ordering': ('condition',),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Customer',
            },
        ),
        migrations.CreateModel(
            name='QuantityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_type', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='RepairCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'MRO',
                'verbose_name_plural': "MRO's",
                'ordering': ('company',),
            },
        ),
        migrations.CreateModel(
            name='Shelve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelve_number', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Shelf',
                'verbose_name_plural': 'Shelves',
            },
        ),
        migrations.CreateModel(
            name='StoreStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
                'ordering': ('first_name',),
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'verbose_name': 'Warehouse',
                'verbose_name_plural': 'Warehouses',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RepairManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_shipped', models.DateField(default=django.utils.timezone.now)),
                ('date_received', models.DateField(blank=True, null=True)),
                ('repair_order', models.CharField(blank=True, max_length=30, null=True)),
                ('component_for_repair', models.OneToOneField(limit_choices_to={'condition_received': '2'}, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.componentinstance')),
                ('condition_received', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.condition')),
                ('repair_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.repaircompany')),
                ('staff_shipped', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.storestaff')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.shelve')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='DespatchNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('despatch_note', models.CharField(blank=True, max_length=30, null=True)),
                ('sizes', models.CharField(blank=True, max_length=30, null=True)),
                ('weight', models.CharField(blank=True, max_length=30, null=True)),
                ('notes', models.CharField(blank=True, max_length=30, null=True)),
                ('despatched_unit', models.ManyToManyField(to='StoreManagement.componentshipment')),
            ],
        ),
        migrations.AddField(
            model_name='componentshipment',
            name='scrapped_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.repaircompany'),
        ),
        migrations.AddField(
            model_name='componentshipment',
            name='shipped_component',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.componentinstance'),
        ),
        migrations.AddField(
            model_name='componentshipment',
            name='shipped_condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.condition'),
        ),
        migrations.AddField(
            model_name='componentshipment',
            name='staff_shipped',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.storestaff'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='condition_received',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.condition'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.customer'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.location'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='staff_received',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.storestaff'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='StoreManagement.quantitytype'),
        ),
        migrations.AddField(
            model_name='componentinstance',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_by_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
