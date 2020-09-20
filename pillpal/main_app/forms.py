from django.forms import ModelForm
from .models import Dosing, Note

class DosingForm(ModelForm):
    class Meta:
        model = Dosing
        fields = ['date', 'time']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['date', 'content']