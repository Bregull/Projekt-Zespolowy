from django.shortcuts import render
import requests
from django.http import HttpResponse
import sys, os
from subprocess import run,PIPE




def button(request):
    return render(request,'home1.html')



def external(request):

     inp= request.POST.get('param')

     out= run([sys.executable, 'C:/Users/Damian/Desktop/Dolby/Projekt-Zespolowy/Katalog/data_input.py',inp],shell=False,stdout=PIPE)

     print(out)


     return render(request,'external.html',{'data1':out.stdout})
     
def home1(request):
    return render(request,'home1.html',)

def zespol(request):
    return render(request,'zespol.html')