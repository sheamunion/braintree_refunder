from django.shortcuts import redirect, render

from .forms import RefunderForm

def new_refund(request):
    form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def start_refund(request):
    if request.method == 'POST':
        form = RefunderForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect('/refunding')
    else: 
        form = RefunderForm()
    return render(request, 'home.html', {'form': form})

def refunding(request):
    return render(request, 'refunding.html')

