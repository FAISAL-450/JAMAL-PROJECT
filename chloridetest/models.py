from django.db import models

class ChlorideTestReading(models.Model):
    time_interval_min = models.IntegerField()
    current_ma = models.DecimalField(max_digits=6, decimal_places=2)
    voltage_v = models.DecimalField(max_digits=5, decimal_places=2)
    charge_passed_coulombs = models.DecimalField(max_digits=8, decimal_places=2)
    specimen_diameter_in = models.DecimalField(max_digits=4, decimal_places=2)
    chloride_ion_permeability = models.CharField(max_length=100)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.time_interval_min} min | {self.chloride_ion_permeability}"


