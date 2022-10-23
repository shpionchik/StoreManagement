from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
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



class Warehouse(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"


class Case(models.Model):
    code = models.CharField(max_length=50, unique=True)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Case"
        verbose_name_plural = "Cases"


class Shelve(models.Model):
    order_number = models.PositiveSmallIntegerField(unique=True)
    case = models.ForeignKey('Case', on_delete=models.CASCADE)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Shelf"
        verbose_name_plural = "Shelves"
        ordering = ('order_number',)


class Customer(models.Model):
    customer = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.customer}"

    class Meta:
        verbose_name = "Customer"


class StoreStaff(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
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


class Status(models.Model):
    condition = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.condition}"

    class Meta:
        verbose_name = "Condition/Status"
        verbose_name_plural = "Statuses"
        ordering = ('condition',)


class Component(models.Model):
    description = models.CharField(max_length=30)
    part_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - {self.part_number}"

    class Meta:
        verbose_name = "ComponentAbstract"
        verbose_name_plural = "ComponentsAbstract"
        ordering = ('part_number',)


class ComponentInstance(models.Model):
    component = models.ForeignKey('Component', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, unique=True)
    status = models.ManyToManyField("Status")
    date_received = models.DateField(auto_now=False, auto_now_add=False)
    received_from = models.CharField(max_length=30)
    staff_received = models.ManyToManyField("StoreStaff", related_name='staff_received')
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id':self.pk})

    def __str__(self):
        return f"{self.component} - {self.serial_number}"

    class Meta:
        verbose_name = "Component"
        verbose_name_plural = "Components"
        ordering = ('component',)


class ComponentCard(models.Model):
    component = models.ForeignKey('ComponentInstance', on_delete=models.CASCADE)
    date_shipped = models.DateField(auto_now=False, auto_now_add=False)
    shipped_to = models.CharField(max_length=30)
    shipped_status = models.ManyToManyField("Status")
    invoice = models.CharField(max_length=30)
    staff_shipped = models.ManyToManyField("StoreStaff", related_name='staff_shipped')


class RepairManagement(models.Model):
    component = models.ForeignKey('ComponentInstance', on_delete=models.CASCADE)
    repair_company = models.ForeignKey('RepairCompany', on_delete=models.CASCADE)
    date_shipped = models.DateField(auto_now=False, auto_now_add=False)
    date_received = models.DateField(auto_now=False, auto_now_add=False)
    staff = models.ForeignKey('StoreStaff', on_delete=models.CASCADE)
    condition_received = models.ForeignKey('Status', on_delete=models.CASCADE)
