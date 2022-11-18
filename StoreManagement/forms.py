from django import forms
from .models import ComponentShipment, ComponentInstance


class DespatchNoteChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    despatched_unit = forms.ModelMultipleChoiceField(queryset=ComponentShipment.objects.all(), required=False)

class ReceivedForm(forms.ModelForm):
    class Meta:
        model = ComponentInstance
        fields = ['component', 'serial_number', 'customer', 'condition_received', 'date_received', 'received_from',
                  'staff_received', 'quantity', 'unit', 'location', 'certificate_number', 'shelf_life',
                  'us_part_condition', 'notes', 'certificate']