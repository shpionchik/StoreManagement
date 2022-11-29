import django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from import_export import results


"""
    Warehouse:
        - id
        - warehouse name
    Case (contains section):
        - id
        - code (unique)
        - warehouse (FK -> Warehouse)
    Shelve (contains shelves):
        - id
        - order number
        - case (FK -> Case)
        - warehouse (FK -> Warehouse)
    Customer (owner):
        - id
    StoreStaff:
        - id
        - name
        - female
    RepairCompany:
        - id 
        - Company_name
     Status:
        - id
        - condition    
    Component:
        - id
        - customer (FK -> Customer)
        - Description
        - Part Number
    ComponentCopy:
        - id
        - component (FK -> Component)
        - serial number
        - status (m2m -> Status)
     ComponentCard:
        - id
        - component_copy (FK -> ComponentCopy)
        - date received
        - received from
        - date shipped
        - shipped to
        - shipped status     
  Shipping (components released):
        - id
        - component_copy (FK -> component)  or O2O?
        - date shipped
        - shipped_by (FK -> StoreStaff) 
        - invoice
    RepairManagement (components send for maintenance):
        - id
        - component_copy (FK -> component)
        - repair company (FK -> RepairCompany)
        - date send for maintenance
        - date received for maintenance
        - sent_by (FK -> StoreStaff)
        - condition received (FK -> Status) 
"""


class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        VIEWER = "VIEWER", "Viewer"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

class StaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return results.filter(role=CustomUser.Role.STAFF)

class Staff(CustomUser):
    base_role = CustomUser.Role.STAFF

    staff = StaffManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 'only for staff'

class ViewerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return results.filter(role=CustomUser.Role.VIEWER)

class Viewer(CustomUser):
    base_role = CustomUser.Role.STAFF

    viewer = ViewerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 'only for users'

class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


class Shelf(models.Model):
    shelf_number = models.CharField(max_length=30, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Shelf"
        verbose_name_plural = "Shelves"



class Customer(models.Model):
    customer = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.customer}"

    class Meta:
        verbose_name = "Customer"


class StoreStaff(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # phone = PhoneNumberField(null=False, blank=False, unique=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"
        ordering = ('first_name',)


class RepairCompany(models.Model):
    company = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.company}"

    class Meta:
        verbose_name = "MRO"
        verbose_name_plural = "MRO's"
        ordering = ('company',)


class Condition(models.Model):
    condition = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.condition}"

    class Meta:
        verbose_name = "Condition"
        verbose_name_plural = "Conditions"
        ordering = ('condition',)


class Component(models.Model):
    description = models.CharField(max_length=60)
    part_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.part_number} {self.description}"

    class Meta:
        verbose_name = "ComponentDescription&PN"
        verbose_name_plural = "ComponentDescription&PN"


class QuantityType(models.Model):
    quantity_type = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.quantity_type}'



class ComponentInstance(models.Model):
    component = models.ForeignKey('Component', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, default=1)
    condition_received = models.ForeignKey("Condition", on_delete=models.CASCADE)
    date_received = models.DateField(default=django.utils.timezone.now)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='updated_by_user', null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by_user', null=True, blank=True)
    received_from = models.CharField(max_length=30)
    staff_received = models.ForeignKey("StoreStaff", on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit = models.ForeignKey('QuantityType', on_delete=models.CASCADE, default=1)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE,  null=True, blank=True)
    shelf = models.ForeignKey('Shelf', on_delete=models.CASCADE, null=True, blank=True)
    certificate_number = models.CharField(max_length=50, null=True, blank=True)
    shelf_life = models.CharField(max_length=50, null=True, blank=True)
    us_part_condition = models.CharField(max_length=50, null=True, blank=True, default='Repairable')
    notes = models.CharField(max_length=50, null=True, blank=True)
    certificate = models.FileField(upload_to='certificate/%Y/%m/%d/', blank=True, null=True)


    def __str__(self):
        return f"{self.serial_number} {self.component} {self.condition_received} {'received'} {self.date_received}"

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ('component',)


class ComponentShipment(models.Model):
    shipped_component = models.OneToOneField('ComponentInstance', on_delete=models.CASCADE)
    shipped_quantity = models.PositiveSmallIntegerField(default=1)
    unit = models.ForeignKey('QuantityType', on_delete=models.CASCADE, default=1)
    date_shipped = models.DateField(default=django.utils.timezone.now)
    shipped_to = models.CharField(max_length=30, null=True, blank=True)
    shipped_condition = models.ForeignKey("Condition", on_delete=models.CASCADE)
    invoice = models.CharField(max_length=30, null=True, blank=True)
    staff_shipped = models.ForeignKey("StoreStaff", on_delete=models.CASCADE, null=True, blank=True)
    scrapped_company = models.ForeignKey('RepairCompany', on_delete=models.CASCADE, null=True, blank=True)
    shipping_order_notes = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.shipped_component} {self.date_shipped} {self.shipped_to}'


class RepairManagement(models.Model):
    component_for_repair = models.OneToOneField('ComponentInstance', on_delete=models.CASCADE,
                                             limit_choices_to={'condition_received': '2'}, unique=True)
    repair_company = models.ForeignKey('RepairCompany', on_delete=models.CASCADE)
    date_shipped = models.DateField(default=django.utils.timezone.now)
    staff_shipped = models.ForeignKey('StoreStaff', on_delete=models.CASCADE)
    date_received = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    condition_received = models.ForeignKey('Condition', on_delete=models.CASCADE, null=True, blank=True)
    repair_order = models.CharField(max_length=30, null=True, blank=True)


class DespatchNote(models.Model):
    despatch_note = models.CharField(max_length=30, null=True, blank=True)
    despatched_unit = models.ManyToManyField('ComponentShipment')
    sizes = models.CharField(max_length=30, null=True, blank=True)
    weight = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=30, null=True, blank=True)

