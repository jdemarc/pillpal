from django.shortcuts import render, redirect
from .models import Prescription, Medication, EmergencyContact

# Form import(s)
from .forms import DosingForm, NoteForm, MedicationForm

# CBV imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Login imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# For API requests
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

def main(request):
    return render(request, 'main.html')

@login_required
def prescriptions_index(request):
    prescriptions = Prescription.objects.filter(user=request.user)
    
    return render(request, 'prescriptions/index.html',
    { 'prescriptions': prescriptions })

@login_required
def prescriptions_detail(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    dosing_form = DosingForm()
    note_form = NoteForm()

    return render(request, 'prescriptions/detail.html',
    { 'prescription': prescription, 'dosing_form': dosing_form, 'note_form': note_form })

@login_required
def add_dosing(request, prescription_id):
    form = DosingForm(request.POST)
    if form.is_valid():
        new_dosing = form.save(commit=False)
        new_dosing.prescription_id = prescription_id
        new_dosing.save()
    return redirect('detail', prescription_id=prescription_id)
    
@login_required
def add_note(request, prescription_id):
    form = NoteForm(request.POST)
    if form.is_valid():
        new_note = form.save(commit=False)
        new_note.prescription_id = prescription_id
        new_note.save()
    return redirect('detail', prescription_id=prescription_id)

@login_required
def add_medication(request, prescription_id):
    form = MedicationForm(request.POST)
    if form.is_valid():
        new_medication = form.save(commit=False)
        new_medication.prescription_id = prescription_id
        new_medication.save()
    return redirect('detail', prescription_id=prescription_id)

@login_required
def remove_medication(request, prescription_id):
    Medication.objects.filter(prescription=prescription_id).delete()

    return redirect('detail', prescription_id=prescription_id)

def medications_search(request, prescription_id):
    search = request.POST.get('search')

    if search:
        search = search.replace(' ', '-')
        response = requests.get('https://api.fda.gov/drug/ndc.json?search=generic_name:%s&limit=5' % search)
        medication = response.json()
        medication_form = []

        limit = len(medication)

        for i in range(0, limit):
            medication_form.append(MedicationForm(initial={
                'brand_name': medication['results'][i]['brand_name'],
                'generic_name': medication['results'][i]['generic_name'],
                'product_ndc': medication['results'][i]['product_ndc'],
                'description': medication['results'][i]['packaging'][0]['description'],
                'active_ingredient': medication['results'][i]['active_ingredients'][0]['name'],
                'dosage_form': medication['results'][i]['dosage_form'],
                'strength': medication['results'][i]['active_ingredients'][0]['strength']
            }))

        return render(request, 'search.html',
        {'medication': medication['results'],
        'medication_form': medication_form, 'prescription_id': prescription_id})

    else:
        return render(request, 'search.html')

@login_required
def medication_assoc(request, ndc):
    prescriptions = Prescription.objects.filter(user=request.user)

    return render(request, 'medications/attach_form.html',
    {'ndc': ndc, 'prescriptions': prescriptions})

'''
Emergency Contact Functions
'''

@login_required
def emergency_contact_detail(request):
    emergency_contact = EmergencyContact.objects.filter(user=request.user)

    return render(request, 'emergency_contact/detail.html', { 'emergency_contact': emergency_contact })

'''
Emergency Contact CRUD
'''
class EmergencyContactCreate(LoginRequiredMixin, CreateView):
    model = EmergencyContact
    fields = ['name', 'phone_number', 'relationship']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url='/emergency_contact/'

class EmergencyContactUpdate(LoginRequiredMixin, UpdateView):
    model = EmergencyContact
    fields = ['name', 'phone_number', 'relationship']

    success_url='/emergency_contact/'

class EmergencyContactDelete(LoginRequiredMixin, DeleteView):
    model = EmergencyContact
    success_url='/emergency_contact/'

'''
Prescription CRUD
'''
class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['rx_number', 'prescription_issue_date', 'prescription_filled_date', 'instructions',
    'delivery', 'dosage', 'refills']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = '/prescriptions/'

class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    model = Prescription
    fields = ['rx_number', 'prescription_issue_date', 'prescription_filled_date', 'instructions',
    'delivery', 'dosage', 'refills']

class PrescriptionDelete(LoginRequiredMixin, DeleteView):
    model = Prescription
    success_url = '/prescriptions/'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)