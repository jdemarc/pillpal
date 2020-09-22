from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class Prescription(models.Model):
    rx_number = models.IntegerField()
    prescription_issue_date = models.DateField()
    prescription_filled_date = models.DateField()
    times_per_day = models.IntegerField()
    delivery = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    refills = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'prescription_id': self.id})

    def taken_today(self):
        return self.dosing_set.filter(date=date.today()).count() >= self.times_per_day
        
    def times_taken(self):
        return self.times_per_day - self.dosing_set.filter(date=date.today()).count()

        
class Dosing(models.Model):
    date = models.DateField('Administration Date')
    time = models.TimeField()

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} at {self.time}"
    
    class Meta:
        ordering = ['-date']

class Note(models.Model):
    date = models.DateField('Note Date')
    content = models.CharField(max_length=250)

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']

class Medication(models.Model):
    brand_name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    product_ndc = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    strength = models.CharField(max_length=100)
    active_ingredient = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=15)

    user = models.OneToOneField(User, on_delete=models.CASCADE)