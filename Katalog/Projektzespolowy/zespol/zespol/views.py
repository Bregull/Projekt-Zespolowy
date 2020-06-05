from django.shortcuts import render
import requests

import sys


from subprocess import run,PIPE

def button(request):
    return render(request,'home.html')


def external(request):

     inp= request.POST.get('param')

     out= run([sys.executable,'C:/Users/pola/Desktop/Projekt/Katalog/data_input.py',inp],shell=False,stdout=PIPE)

     print(out)


     return render(request,'home.html',{'data1':out.stdout})
