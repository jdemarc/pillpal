from django.shortcuts import render, redirect
from .models import Prescription

# Form import(s)
from .forms import DosingForm, NoteForm

# CBV imports
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Login imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# For API requests
import requests
from .services import get_medications #Maybe we do not need

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

def medications_search(request):
    search = request.POST.get('search')

    if search:
        search = search.replace(' ', '-')
        print(search)
        response = requests.get('https://api.fda.gov/drug/ndc.json?search=generic_name:%s&limit=5' % search)
        medication = response.json()
        return render(request, 'search.html',
        {'medication': medication['results']})

    else:
        return render(request, 'search.html')

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