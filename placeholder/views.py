from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import MilageInstance, MilageForm, Car, CarForm
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import csv


@login_required(login_url='/')
def index(request):
    car = Car.objects.all().filter(user=request.user)
    if request.method == 'POST':

        form = MilageForm(data=request.POST, user=request.user)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.user = request.user
            new_obj.save()
            form = MilageForm(request.user)

    else:
        form = MilageForm(request.user)

    latest = MilageInstance.objects.filter(user=request.user)[0:3]
    template = 'placeholder/milage-index.html'
    context = {
        'car': car,
        'form': form,
        'latest': latest,
    }

    return render(request, template, context)


@login_required(login_url='/')
def history(request):
    query = MilageInstance.objects.filter(user=request.user)
    template = 'placeholder/history.html'
    context = {
        'query': query,
    }
    return render(request, template, context)


@login_required(login_url='/')
def delete(request, id):
    obj = MilageInstance.objects.filter(pk=id, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def overview(request):

    context = {}

    query = MilageInstance.objects.filter(user=request.user)
    query_length = query.count()

    # Total km driven
    #### STATS
    # total_km
    # total_liters
    # total_amount
    # total_refills
    # avg_amount
    # avg_liter
    # km_per_liter
    # amount_per_liter


    # TOTALs:
    total_km = 0
    total_liters = 0
    total_amount = 0

    # chart data
    hs_price_per_liter = []
    hs_km_per_liter = []
    hs_dates = []

    for q in query:
        total_km = total_km + q.trip()
        total_liters = total_liters + q.liter
        total_amount = total_amount + q.amount
        hs_price_per_liter.append(q.amount_pr_liter())
        hs_km_per_liter.append(q.km_pr_liter())
        hs_dates.append(q.date)

    # reverse order for chart
    hs_price_per_liter = hs_price_per_liter[::-1]
    hs_km_per_liter = hs_km_per_liter[::-1]
    hs_dates = hs_dates[::-1]

    total_refills = query_length

    # AVGs:
    if query_length != 0:
        avg_amount = total_amount / query_length
        avg_liter = total_liters / query_length
    else:
        avg_amount = 0
        avg_liter = 0

    context = {
        'total_km': total_km,
        'total_liters': total_liters,
        'total_amount': total_amount,
        'hs_price_per_liter': hs_price_per_liter,
        'hs_km_per_liter': hs_km_per_liter,
        'hs_dates': hs_dates,
        'total_refills': total_refills,
        'avg_amount': avg_amount,
        'avg_liter': avg_liter,
    }

    template = 'placeholder/overview.html'
    return render(request, template, context)


def get_date(date, format):
    split = date.split('/')
        # check date format
    if (format == 'dd/mm/yyyy'):
        day = split[0]
        month = split[1]
        year = split[2]
    elif (format == 'mm/dd/yyyy'):
        day = split[1]
        month = split[0]
        year = split[2]
    elif (format == 'yyyy/dd/mm'):
        day = split[1]
        month = split[2]
        year = split[0]
    else: # date format is yyyy/mm/dd
        day = split[2]
        month = split[1]
        year = split[0]
    return '-'.join([year, month, day])


def handle_uploaded_file(user, date_format, f):
    with open('user_data/{}-data.csv'.format(user), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open('user_data/{}-data.csv'.format(user), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        print(headers)
        for row in reader:
            to_add = {
                headers[0]: row[0],
                headers[1]: row[1],
                headers[2]: row[2],
                headers[3]: row[3],
            }
            print(to_add)
            new_instance = MilageInstance.create(
                date=get_date(to_add['date'], date_format),
                km_stand=to_add['km'],
                amount=to_add['cost'],
                liter=to_add['liter'],
                user=user
            )
            new_instance.save()

@login_required(login_url='/')
def upload_csv(request):
    form = UploadFileForm
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            date_format = cleaned_data['date_format']
            handle_uploaded_file(request.user, date_format, request.FILES['file'])
            return HttpResponseRedirect('/milage/history')
    return render(request, 'placeholder/upload.html', {'form': form})


@login_required(login_url='/')
def clear_history(request):
    MilageInstance.objects.filter(user=request.user).delete()
    return HttpResponseRedirect('upload')


@login_required(login_url='/')
def edit(request, instance_id):
    instance = MilageInstance.objects.get(pk=instance_id)
    if request.method == 'GET':
        if instance.user != request.user:
            return HttpResponseRedirect('404.html')
        form = MilageForm(user=request.user, initial={
            'date': instance.date,
            'km_stand': instance.km_stand,
            'amount': instance.amount,
            'liter': instance.liter
        })
        return render(request, 'placeholder/edit.html', {'form': form, 'pk': instance_id})
    elif request.method == 'POST' and request.user == instance.user:
        updated_form = MilageForm(request.POST, user=request.user)
        if updated_form.is_valid():
            cleaned_data = updated_form.cleaned_data
            instance.date = cleaned_data['date']
            instance.km_stand = cleaned_data['km_stand']
            instance.amount = cleaned_data['amount']
            instance.liter = cleaned_data['liter']
            instance.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('404.html')


def cars(request):
    form = CarForm()
    registered_cars = Car.objects.all().filter(user=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            try:
                car = form.save(commit=False)
                car.registration_no = car.registration_no.upper() # Upper case letters!
                car.user = request.user
                car.save()
                form = CarForm()
            except IntegrityError:
                form.add_error('registration_no', 'You already have a car with that registration number')

    context = {
        'form': form,
        'registered_cars': registered_cars,
    }
    return render(request, 'placeholder/cars.html', context)


