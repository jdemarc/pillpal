from django.shortcuts import render, redirect
from .models import Prescription

# CBV imports
from django.views.generic.edit import CreateView

# Login imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
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
    prescriptions = Prescription.objects.get(id=prescription_id)
    return render(request, 'prescriptions/detail.html',
    { 'prescriptions': prescriptions })

class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['prescription_issue_date', 'prescription_filled_date', 'instructions',
    'delivery', 'dosage', 'refills']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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