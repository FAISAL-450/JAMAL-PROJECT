from django import forms
from django.contrib.auth.models import User
from .models import Customerbill
from customerdetailed.models import CustomerDetailed
from project.models import Project

class CustomerbillForm(forms.ModelForm):
    class Meta:
        model = Customerbill
        fields = [
            'project_name',
            'customer_name',
            'description_bill',
            'bill_date',
            'bill_no',
            'bill_amount',
        ]
        labels = {
            'project_name': 'Project Name',
            'customer_name': 'Customer Name',
            'description_bill': 'Description of Bill',
            'bill_date': 'Bill Date',
            'bill_no': 'Bill No',
            'bill_amount': 'Bill Amount',
        }
        widgets = {
            'project_name': forms.Select(attrs={'class': 'form-control'}),
            'customer_name': forms.Select(attrs={'class': 'form-control'}),
            'description_bill': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bill description'
            }),
            
            'bill_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'bill_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bill no'
            }),
            
            'bill_amount': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bill amount'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['project_name'].empty_label = "--------- Select Project Name ---------"
        self.fields['customer_name'].empty_label = "--------- Select Customer Name ---------"

        # 🔐 Show only projects created by-Jasim
        jasim_email = 'jasim@dzignscapeprofessionals.onmicrosoft.com'
        try:
            jasim_user = User.objects.get(email__iexact=jasim_email)
            self.fields['project_name'].queryset = Project.objects.filter(created_by=jasim_user)
        except User.DoesNotExist:
            self.fields['project_name'].queryset = Project.objects.none()

        # 🎯 Filter customer names created by the current user (based@dzignscapeprofessionals.onmicrosoft.com)
        if user:
            self.fields['customer_name'].queryset = CustomerDetailed.objects.filter(created_by=user)
        else:
            self.fields['customer_name'].queryset = CustomerDetailed.objects.none()




