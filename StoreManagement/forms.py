from django import forms
from .models import ComponentShipment


class DespatchNoteChangeListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    despatched_unit = forms.ModelMultipleChoiceField(queryset=ComponentShipment.objects.all(), required=False)
