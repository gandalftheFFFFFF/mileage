from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from placeholder.views import index as milage_index


def index(request):

    if request.method == 'POST':
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('placeholder.views.index')
    elif request.user.is_authenticated():
        return redirect('placeholder.views.index')
    else:
        form = AuthenticationForm()

    template = 'login.html'

    context = {
        'form': form,
    }
    return render(request, template, context)


def create_user(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render(request, 'login.html', {'form': AuthenticationForm(),})
    else:
        form = UserCreationForm()

    template = 'create-user.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
