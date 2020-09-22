from django.contrib import admin

from .models import Prescription, Dosing, Note, Medication, EmergencyContact, Photo

# Register your models here.
admin.site.register(Prescription)
admin.site.register(Dosing)
admin.site.register(Note)
admin.site.register(Medication)
admin.site.register(EmergencyContact)
admin.site.register(Photo)