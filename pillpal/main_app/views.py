from django.shortcuts import render, redirect
from .models import Prescription

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