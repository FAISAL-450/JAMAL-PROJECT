from django import forms
from .models import Contractor

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = [
            'contractor_company',
            'name_of_contractor',
            'contractor_address',
            'contractor_phone_number',
        ]

        labels = {
            'contractor_company': 'Contractor Company',
            'name_of_contractor': 'Contractor Name',
            'contractor_address': 'Contractor Address',
            'contractor_phone_number': 'Phone Number',
        }

        widgets = {
            'contractor_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contractor company name'
            }),
            'name_of_contractor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contractor name'
            }),
            'contractor_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contractor address'
            }),
            'contractor_phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
        }
