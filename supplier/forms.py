from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'name_of_supplier',
            'supplier_address',
            'supplier_contact_person',
            'supplier_contact_number',
        ]

        labels = {
            'name_of_supplier': 'Supplier Name',
            'supplier_address': 'Supplier Address',
            'supplier_contact_person': 'Contact Person Name',
            'supplier_contact_number': 'Contact Person Number',
        }

        widgets = {
            'name_of_supplier': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier name'
            }),
            'supplier_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter supplier address'
            }),
            'supplier_contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact person name'
            }),
            'supplier_contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact number'
            }),
        }
