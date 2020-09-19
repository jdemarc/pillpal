from django.shortcuts import render, redirect
from .models import Prescription

from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse('<h1>Home</h1>')

def main(request):
    return render(request, 'main.html')

def prescriptions_index(request):
    prescriptions = Prescription.objects.all()
    
    return render(request, 'prescriptions/index.html',
    { 'prescriptions': prescriptions })
