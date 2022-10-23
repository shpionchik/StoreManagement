from django.contrib import admin
from django.urls import path, include
from .models import Warehouse, Case, Shelve, Customer, Component, RepairCompany, Status, StoreStaff, ComponentInstance


@admin.register(Warehouse)
@admin.register(Case)
@admin.register(Shelve)
@admin.register(Customer)
@admin.register(Component)
@admin.register(RepairCompany)
@admin.register(Status)
@admin.register(StoreStaff)
@admin.register(ComponentInstance)

class WarehouseAdmin(admin.ModelAdmin):
    pass


class CaseAdmin(admin.ModelAdmin):
    pass


class ShelveAdmin(admin.ModelAdmin):
    pass