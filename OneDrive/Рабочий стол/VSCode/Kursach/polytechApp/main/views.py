from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    render(request,'main/index.html')

def catalog(request):
    render(request,'main/catalog.html')

