from django.shortcuts import render, redirect

from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse('<h1>Home</h1>')

def main(request):
    return render(request, 'main.html')