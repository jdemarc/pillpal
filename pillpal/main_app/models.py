from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class Prescription(models.Model):
    prescription_issue_date = models.DateField()
    prescription_filled_date = models.DateField()
    instructions = models.CharField(max_length=250)
    delivery = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    refills = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'prescription_id': self.id})
        
class Dosing(models.Model):
    date = models.DateField('Administration Date')
    time = models.TimeField()

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} at {self.time}"

# class Medication(models.Model):
#     brand_name = models.CharField(max_length=100)
#     generic_name = models.CharField(max_length=100)
#     product_ndc = models.CharField(max_length=100)
#     side_effects = models.CharField(max_length=300)

