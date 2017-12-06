from django.shortcuts import redirect, render
import csv

from .forms import RefunderForm
from refunder.refund_job import RefundJob

def new_refund(request):
    form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def start_refund(request):
    if request.method == 'POST':
        form = RefunderForm(request.POST, request.FILES)
        if form.is_valid():
            keys = [
                form.cleaned_data['environment'], 
                form.cleaned_data['merchant_id'], 
                form.cleaned_data['public_key'], 
                form.cleaned_data['private_key'],
            ]
            job = RefundJob(keys)
            decoded_file = form.cleaned_data['source_csv'].read().decode('utf-8').splitlines()

            job.run(decoded_file)
            
            return redirect('/refunding')
    else: 
        form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def refunding(request):
    return render(request, 'refunding.html')

