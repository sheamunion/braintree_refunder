from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RefunderForm

def index(request):
    if request.method == 'POST':
        form = RefunderForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponseRedirect('/refunding')
    else:
        form = RefunderForm()

    return render(request, 'home.html', {'form': form})

def refunding(request):
        return render(request, 'refunding.html')
