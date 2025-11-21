from django import forms
from .models import ChlorideTestReading

class ChlorideTestReadingForm(forms.ModelForm):
    class Meta:
        model = ChlorideTestReading
        fields = [
            'time_interval_min',
            'current_ma',
            'voltage_v',
            'charge_passed_coulombs',
            'specimen_diameter_in',
            'chloride_ion_permeability',
            'remarks',
        ]

        labels = {
            'time_interval_min': 'Time Interval (minutes)',
            'current_ma': 'Current (mA)',
            'voltage_v': 'Voltage (V)',
            'charge_passed_coulombs': 'Charge Passed (Coulombs)',
            'specimen_diameter_in': 'Specimen Diameter (inches)',
            'chloride_ion_permeability': 'Chloride Ion Permeability',
            'remarks': 'Remarks',
        }

        widgets = {
            'time_interval_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter time interval in minutes'
            }),
            'current_ma': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter current in mA'
            }),
            'voltage_v': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter voltage in V'
            }),
            'charge_passed_coulombs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter charge passed in coulombs'
            }),
            'specimen_diameter_in': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter specimen diameter in inches'
            }),
            'chloride_ion_permeability': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter chloride ion permeability classification'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter optional remarks',
                'rows': 3
            }),
        }

