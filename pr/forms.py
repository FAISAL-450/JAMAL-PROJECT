from django import forms
from .models import Pr
from .models import Project
from .models import Resource

class PrForm(forms.ModelForm):
    class Meta:
        model = Pr
        fields = [
            'project_name_pr',
            'requisition_date_pr',
            'requisition_no',
            'resource_name_pr',
            'unit_resource_pr',
            'quantity_pr',
            'delivery_date_pr',
            'remarks',
        ]

        labels = {
            'project_name_pr': 'Project Name',
            'requisition_date_pr': 'Requisition Date',
            'requisition_no': 'Requisition Number',
            'resource_name_pr': 'Resource Name',
            'unit_resource_pr': 'Unit',
            'quantity_pr': 'Quantity',
            'delivery_date_pr': 'Delivery Date',
            'remarks': 'Remarks',
        }

        widgets = {
            'project_name_pr': forms.Select(attrs={
                'class': 'form-control',
            }),
            'requisition_date_pr': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'requisition_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter requisition number',
            }),
            'resource_name_pr': forms.Select(attrs={
                'class': 'form-control',
            }),
            'unit_resource_pr': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter unit (e.g., pcs, kg)',
            }),
            'quantity_pr': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
            }),
            'delivery_date_pr': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'remarks': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter remarks',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Whole-Project-Drop-down
        # Empty label for-project-dropdown
        self.fields['project_name_pr'].empty_label = "--------- Select Project Name ---------"
        # ✅ Filter-projects-by logged-in user
        if user:
            queryset = Project.objects.filter(created_by=user)
        else:
            queryset = Project.objects.none()

        # Preserve selected-project-during edit
        if self.instance.pk and self.instance.project_name_pr:
            selected = Project.objects.filter(pk=self.instance.project_name_pr.pk)
            queryset = (queryset | selected).distinct()
        self.fields['project_name_pr'].queryset = queryset

        # Whole-Resource-Drop-down
        # Empty label for-resource-dropdown
        self.fields['resource_name_pr'].empty_label = "--------- Select Resource Name ---------"

        # ✅ Filter-resources-by logged-in user
        if user:
            queryset = Resource.objects.filter(created_by=user)
        else:
            queryset = Resource.objects.none()

        # Preserve selected-resource-during edit
        if self.instance.pk and self.instance.resource_name_pr:
            selected = Resource.objects.filter(pk=self.instance.resource_name_pr.pk)
            queryset = (queryset | selected).distinct()
        self.fields['resource_name_pr'].queryset = queryset
