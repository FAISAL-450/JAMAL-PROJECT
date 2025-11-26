from django import forms
from .models import RequisitionItem, Project

class RequisitionItemForm(forms.ModelForm):
    # ✅ Add total_amount as a disabled field (read-only)
    total_amount = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        label="Total Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        })
    )

    class Meta:
        model = RequisitionItem
        fields = [
            'project_name_fpr',
            'PR_date',
            'PR_no',
            'name_of_resource',
            'resource_unit',
            'quantity',
            'unit_price',
            'status',
            
        ]

        labels = {
            'project_name_fpr': 'Project Name',
            'PR_date': 'PR Date',
            'PR_no': 'PR Number',
            'name_of_resource': 'Resource Name',
            'resource_unit': 'Unit',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price',
            'status': 'Status',
            'total_amount': 'Total Amount',
        }

        widgets = {
            'project_name_fpr': forms.Select(attrs={'class': 'form-control'}),
            'PR_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'PR_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PR number'}),
            'name_of_resource': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resource name'}),
            'resource_unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit (e.g., kg, pcs)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit price'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['project_name_fpr'].empty_label = "--------- Select Project Name ---------"

        # Define allowed emails for dropdown access
        allowed_emails = [
            'jasim@dzignscapeprofessionals.onmicrosoft.com',
            'lemon@dzignscapeprofessionals.onmicrosoft.com',
        ]
        normalized_emails = [email.lower().strip() for email in allowed_emails]

        # Filter queryset based on user
        if user and user.email.lower().strip() in normalized_emails:
            queryset = Project.objects.filter(created_by=user)
        else:
            queryset = Project.objects.none()

        # Preserve selected value during edit
        if self.instance.pk and self.instance.project_name_fpr:
            selected = Project.objects.filter(pk=self.instance.project_name_fpr.pk)
            queryset = selected | queryset

        self.fields['project_name_fpr'].queryset = queryset

        # ✅ Pre-fill total_amount from instance (calculated in model.save)
        if self.instance.pk:
            self.fields['total_amount'].initial = self.instance.total_amount
        else:
            self.fields['total_amount'].initial = 0
