from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from management.admin import UploadForm,TestForm

def home(request):
    return render(request,'home.html',{})

def uploadMultiple(request):
    if request.method == 'POST':
       form = UploadForm(request.POST, request.FILES)
   
       if form.is_valid():
        form.process(request)
        pass
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form.as_p, })

def test(request):
    if request.method == 'POST':
       form = TestForm(request.POST, request.FILES)
   
       if form.is_valid():
        form.process(request)
        pass
    else:
        form = TestForm()
    return render(request, 'test.html', {'form': form.as_p, })