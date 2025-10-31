from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'account_name',
            'account_code',
            'account_type',
            'account_description',
            'currency',
            'cost_center',
            'status',
        ]

        labels = {
            'account_name': 'Account Name',
            'account_code': 'Account Code',
            'account_type': 'Account Type',
            'account_description': 'Description',
            'currency': 'Currency',
            'cost_center': 'Cost Center',
            'status': 'Status',
        }

        widgets = {
            'account_name': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select account name'
            }),
            'account_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter account code'
            }),
            'account_type': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select account type'
            }),
            'account_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': 'Enter description'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select currency'
            }),
            'cost_center': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select cost center'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select status'
            }),
        }
