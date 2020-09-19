from django.forms import ModelForm
from .models import Dosing

class DosingForm(ModelForm):
    class Meta:
        model = Dosing
        fields = ['date', 'time']