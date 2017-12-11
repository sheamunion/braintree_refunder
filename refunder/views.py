from django.shortcuts import redirect, render
import csv

from .forms import RefunderForm
from refunder.refund_job import RefundJob

def new_refund(request):
    form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def start_refund(request):
    error = False
    if request.method == 'POST':
        form = RefunderForm(request.POST, request.FILES)
        if form.is_valid():
            keys = [
                form.cleaned_data['environment'], 
                form.cleaned_data['merchant_id'], 
                form.cleaned_data['public_key'], 
                form.cleaned_data['private_key'],
            ]
            decoded_file = form.cleaned_data['source_csv'].read().decode('utf-8').splitlines()
            try:	
                job = RefundJob(keys, decoded_file)
                job.run()
                return redirect('/refunding')
            except TypeError as e:
                error = "API keys are incorrect."
    else: 
        form = RefunderForm()
    return render(request, 'home.html', {'form': form, 'error': error})

def refunding(request):
    return render(request, 'refunding.html')

