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
            'time_interval_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_ma': forms.NumberInput(attrs={'class': 'form-control'}),
            'voltage_v': forms.NumberInput(attrs={'class': 'form-control'}),
            'charge_passed_coulombs': forms.NumberInput(attrs={'class': 'form-control'}),
            'specimen_diameter_in': forms.NumberInput(attrs={'class': 'form-control'}),
            'chloride_ion_permeability': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
