from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Prescription(models.Model):
    prescription_issue_date = models.DateField()
    prescription_filled_date = models.DateField()
    instructions = models.CharField(max_length=250)
    delivery = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    refills = models.IntegerField()