from django import forms
from .models import Project, Contractorbill

class ContractorbillForm(forms.ModelForm):
    # ✅ Add bill_amount as a disabled field (read-only)
    bill_amount = forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        label="Bill Amount",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
        })
    )

    class Meta:
        model = Contractorbill
        fields = [
            'project_name_cb',
            'project_address_cb',
            'contractor_company_name',
            'name_of_work',
            'work_unit',
            'bill_date',
            'bill_no',
            'quantity',
            'unit_price',
        ]

        labels = {
            'project_name_cb': 'Project Name',
            'project_address_cb': 'Project Address',
            'contractor_company_name': 'Contractor Company Name',
            'name_of_work': 'Name of Work',
            'work_unit': 'Work Unit',
            'bill_date': 'Bill Date',
            'bill_no': 'Bill Number',
            'quantity': 'Quantity',
            'unit_price': 'Unit Price',
            'bill_amount': 'Bill Amount',
        }

        widgets = {
            'project_name_cb': forms.Select(attrs={'class': 'form-control'}),
            'project_address_cb': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project address'}),
            'contractor_company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contractor company name'}),
            'name_of_work': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name of work'}),
            'work_unit': forms.Select(attrs={'class': 'form-control'}),
            'bill_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bill_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bill number'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit price'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Empty label for project dropdown
        self.fields['project_name_cb'].empty_label = "--------- Select Project Name ---------"

        # ✅ Filter projects by logged-in user
        if user:
            queryset = Project.objects.filter(created_by=user)
        else:
            queryset = Project.objects.none()

        # Preserve selected project during edit
        if self.instance.pk and self.instance.project_name_cb:
            selected = Project.objects.filter(pk=self.instance.project_name_cb.pk)
            queryset = (queryset | selected).distinct()

        self.fields['project_name_cb'].queryset = queryset

        # ✅ Pre-fill bill_amount from instance (calculated in model.save)
        self.fields['bill_amount'].initial = getattr(self.instance, "bill_amount", 0)
