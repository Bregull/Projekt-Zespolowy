from django.shortcuts import render
import requests
from django.http import HttpResponse
import sys, os
from subprocess import run,PIPE
import os
from os.path import dirname




def button(request):
    return render(request,'home1.html')



def external(request):

     inp= request.POST.get('param')
     path = dirname(dirname(os.getcwd()))
     path = f'{path}/main.py'
     out= run([sys.executable, path,inp],shell=False,stdout=PIPE)

     print(out)

     out_data = out.stdout.decode('ascii')

     return render(request,'external.html',{'data1':out_data})
     
def home1(request):
    return render(request,'home1.html',)

def zespol(request):
    return render(request,'zespol.html')