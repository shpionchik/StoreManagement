from django.contrib import admin
from import_export import resources, widgets, fields
from django.contrib.admin.views.main import ChangeList
from .forms import DespatchNoteChangeListForm
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.resources import Field
from .models import Warehouse, Shelve, Customer, Component, RepairCompany, Condition, StoreStaff, \
    ComponentInstance, RepairManagement, ComponentShipment, QuantityType, Location, CustomUser, DespatchNote


# class CompositeForeignWidget(widgets.ForeignKeyWidget):
#
#     def clean(self, value, row=None, **kwargs):
#         k1 = row['description']
#         k2 = row['part_number']
#         return self.model.objects.get(description=k1, part_number=k2)


class ComponentResource(resources.ModelResource):
    # setting = Field(
    #     widget=CompositeForeignWidget(Component)
    # )
    # component = fields.Field(
    #         column_name= 'Component',
    #         attribute = 'Component',
    #         widget=ForeignKeyWidget(Component, 'Component')
    #     )
    class Meta:
        model = ComponentInstance
        skip_unchanged = True
        report_skipped = True
        # exclude = ('id',)
        import_id_fields = ['id']
        fields = ('id', 'component', 'serial_number', 'quantity', 'received_from', 'staff_received', 'date_received',
                  'condition_received', 'quantity', 'unit', 'location', 'certificate_number', 'shelf_life',
                  'us_part_condition')

    # def get_import_fields(self):
    #     return [self.fields[f] for f in ['description', 'part_number']]


class ComponentAbstractResource(resources.ModelResource):
    class Meta:
        model = Component
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ['id']
        fields = ('id', 'description', 'part_number')


class DespatchNoteChangeList(ChangeList):
    def __init__(self,
                 request,
                 model,
                 list_display,
                 list_display_links,
                 list_filter,
                 date_hierarchy,
                 search_fields,
                 list_select_related,
                 list_per_page,
                 list_max_show_all,
                 list_editable,
                 model_admin,
                 sortable_by,
                 search_help_text): super(DespatchNoteChangeList, self).__init__(request, model, list_display,
                                                                                 list_display_links, list_filter,
                                                                                 date_hierarchy, search_fields,
                                                                                 list_select_related,
                                                                                 list_per_page, list_max_show_all,
                                                                                 list_editable, model_admin,
                                                                                 sortable_by, search_help_text)

    list_display = ['despatch_note', 'despatched_unit', 'sizes', 'weight', 'notes']
    list_display_links = ['despatch_note']
    list_editable = ['despatched_unit']


class DespatchNoteAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return DespatchNoteChangeList

    def get_changelist_form(self, request, **kwargs):
        return DespatchNoteChangeListForm


admin.site.register(DespatchNote, DespatchNoteAdmin)


class ComponentShipmentAdmin(admin.ModelAdmin):
    list_display = ('shipped_component', 'date_shipped', 'shipped_to', 'shipped_condition', 'invoice', 'staff_shipped',
                    'scrapped_company', 'shipping_order_notes')


admin.site.register(ComponentShipment, ComponentShipmentAdmin)


class RepairManagementAdmin(admin.ModelAdmin):
    list_display = ('component_for_repair', 'repair_company', 'date_shipped', 'date_received', 'staff_shipped',
                    'condition_received', 'repair_order')


admin.site.register(RepairManagement, RepairManagementAdmin)


class StoreStaffAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']


admin.site.register(StoreStaff, StoreStaffAdmin)


class RepairCompanyAdmin(admin.ModelAdmin):
    list_display = ['company']


admin.site.register(RepairCompany, RepairCompanyAdmin)


class ShelveAdmin(admin.ModelAdmin):
    list_display = ['shelve_number']


admin.site.register(Shelve, ShelveAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['store', 'shelve']


admin.site.register(Location, LocationAdmin)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Warehouse, WarehouseAdmin)


class ComponentInstanceAdmin(ImportExportModelAdmin):
    list_display = ['id', 'component', 'serial_number', 'quantity', 'received_from', 'date_received', 'staff_received',
                    'condition_received', 'quantity', 'unit', 'location', 'certificate_number', 'shelf_life',
                    'us_part_condition']
    resource_classes = [ComponentResource]


admin.site.register(ComponentInstance, ComponentInstanceAdmin)


class QuantityTypeAdmin(admin.ModelAdmin):
    list_display = ['quantity_type', ]


admin.site.register(QuantityType, QuantityTypeAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer']


admin.site.register(Customer, CustomerAdmin)


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'condition']


admin.site.register(Condition, StatusAdmin)


class ComponentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'description', 'part_number')
    resource_classes = [ComponentAbstractResource]


admin.site.register(Component, ComponentAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)
