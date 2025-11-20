from django import forms
from .models import Proposal

class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = [
            'title',
            'description',
            'industry',
            'client_email',
        ]

        labels = {
            'title': 'Proposal Title',
            'description': 'Proposal Description',
            'industry': 'Industry Type',
            'client_email': 'Client Email',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter proposal title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter proposal description',
                'rows': 4
            }),
            'industry': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter industry type'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter client email'
            }),
        }

# Custom widget to support multiple file uploads
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class DocumentForm(forms.Form):
    file = forms.FileField(
        widget=MultiFileInput(attrs={
            'class': 'form-control',
            'multiple': True
        }),
        label='Upload Document(s)',
        required=False
    )








