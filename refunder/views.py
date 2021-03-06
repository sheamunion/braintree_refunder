from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
import csv, os

from twilio.rest import Client

from .forms import RefunderForm
from refunder.refund_job import RefundJob

def new_refund(request):
    form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def start_refund(request):
    error = None
    if request.method == 'POST':
        form = RefunderForm(request.POST, request.FILES)
        if form.is_valid():
            error = None 
            keys = [
                form.cleaned_data['environment'], 
                form.cleaned_data['merchant_id'], 
                form.cleaned_data['public_key'], 
                form.cleaned_data['private_key'],
            ]
            phone = form.cleaned_data['phone']
            decoded_file = form.cleaned_data['source_csv'].read().decode('utf-8').splitlines()
            try:	
                job = RefundJob(keys, decoded_file)
                log_file_name = job.run(keys[1])
                return redirect(reverse('refunding', args=[log_file_name, phone]))
            except TypeError as e:
                error = e
    else: 
        form = RefunderForm()
    return render(request, 'home.html', {'form': form, 'error': error})

def refunding(request, file_name, phone):
    __send_sms_confirmation(phone)
    context = {'file_name': file_name}
    return render(request, 'refunding.html', context )

def download(request, file_name):
    file_path = '{}/refunder/files/{}'.format(settings.BASE_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
            return response 
    raise Http404

def __send_sms_confirmation(phone):
        us_phone = '1' + phone
        account_sid = os.getenv('TWILIO_SID')
        auth_token = os.getenv('TWILIO_TOKEN')
        client = Client(account_sid, auth_token)
        client.api.account.messages.create(
            to=us_phone,
            from_='+14436489515',
            body='Refund job is complete!')

