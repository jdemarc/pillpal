from django import forms 
from django.forms import ModelForm
from .models import Dosing, Note, Medication, Prescription


class DosingForm(ModelForm):
    date = forms.DateField(label="Administration Date", widget=forms.TextInput(attrs={'id': 'dose_date'}))
    
    class Meta:
        model = Dosing
        fields = ['date', 'time']

class NoteForm(ModelForm):
    date = forms.DateField(label="Note Date", widget=forms.TextInput(attrs={'id': 'note_date'}))
    
    class Meta:
        model = Note
        fields = ['date', 'content']

class MedicationForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['generic_name', 'product_ndc',
        'description', 'dosage_form', 'active_ingredient', 'strength']