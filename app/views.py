from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

    # Check to see if logging in?
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticating given ifo
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error, Please try again...")
            return redirect('home')
    else:
        context = {
            'records': records
        }
        return render(request, 'home.html', context)


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out..')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login in new user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully created an account. Welcome...')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def record_detail(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=pk)
        context = {
            'record': record
        }

        return render(request, 'record_detail.html', context)
    else:
        messages.success(request, 'You must be logged in to view this page')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=pk)
        record.delete()
        messages.success(request, 'You have deleted a Record.')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to do this action.')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record added.")
                return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'add_record.html', context)
    else:
        messages.success(request, "You must be logged in to do this action")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record successfully updated.")
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, 'update_record.html', context)
    else:
        messages.success(request, "You must be logged in to do this action")
        return redirect('home')

