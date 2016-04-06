from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from .models import MilageInstance, MilageForm, Car, CarForm
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import csv


def get_current_car(request):
    # current_car priority:
    # 1: session car
    # 2: latest added car
    user = request.user
    cars = Car.objects.filter(user=user)
    print(cars)
    if cars:
        # User has cars, so either we can get or set a car
        session_car_reg_no = request.session.get('current_car', None)
        if session_car_reg_no is not None:
            try:
                current_car = Car.objects.get(user=user, registration_no=session_car_reg_no)
            except ObjectDoesNotExist:
                current_car = cars[0]
                request.session['current_car'] = current_car.registration_no
        else:
            current_car = cars[0]
            request.session['current_car'] = current_car.registration_no
        return current_car
    else:
        # There are no cars for that user, thus we can clear the session car:
        try:
            del request.session['current_car']
        except KeyError:
            pass
        return None


@login_required(login_url='/')
def index(request):
    cars = Car.objects.all().filter(user=request.user)
    if request.method == 'POST':
        form = MilageForm(data=request.POST, user=request.user, request=request)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.user = request.user
            new_obj.date = timezone.now()
            new_obj.save()
            request.session['current_car'] = new_obj.car.registration_no
            form = MilageForm(user=request.user, request=request)

    else:
        form = MilageForm(user=request.user, request=request)
    current_car = get_current_car(request)
    latest = MilageInstance.objects.filter(user=request.user, car=current_car)[0:3]
    template = 'placeholder/milage-index.html'
    context = {
        'cars': cars,
        'current_car': current_car,
        'form': form,
        'latest': latest,
    }

    return render(request, template, context)


@login_required(login_url='/')
def history(request):
    cars = Car.objects.filter(user=request.user)
    current_car = get_current_car(request)
    query = MilageInstance.objects.filter(user=request.user, car=current_car)
    template = 'placeholder/history.html'
    context = {
        'query': query,
        'cars': cars,
        'current_car': current_car,
    }
    return render(request, template, context)


@login_required(login_url='/')
def delete(request, id):
    obj = MilageInstance.objects.filter(pk=id, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/')
def overview(request):
    cars = Car.objects.filter(user=request.user)
    current_car = get_current_car(request)
    query = MilageInstance.objects.filter(user=request.user).filter(car=current_car)
    query_length = query.count()

    # TOTALs:
    total_km = 0
    total_liters = 0
    total_amount = 0

    # chart data
    hs_price_per_liter = []
    hs_km_per_liter = []
    hs_dates = []

    for q in query:
        total_km = total_km + q.trip() # bad time complexity
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
        'cars': cars,
        'current_car': current_car,
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


def handle_uploaded_file(user, date_format, f, car):
    with open('user_data/{}-data.csv'.format(user), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open('user_data/{}-data.csv'.format(user), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            to_add = {
                headers[0]: row[0],
                headers[1]: row[1],
                headers[2]: row[2],
                headers[3]: row[3],
            }
            new_instance = MilageInstance.create(
                date=get_date(to_add['date'], date_format),
                km_stand=to_add['km'],
                amount=to_add['cost'],
                liter=to_add['liter'],
                user=user,
                car=car,
            )
            new_instance.save()

@login_required(login_url='/')
def upload_csv(request):
    form = UploadFileForm(user=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            date_format = cleaned_data['date_format']
            car = cleaned_data['car']
            print(car)
            handle_uploaded_file(request.user, date_format, request.FILES['file'], car)
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


@login_required
def cars_overview(request):
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
                request.session['current_car'] = car.registration_no # set new current car
                form = CarForm()
            except IntegrityError:
                form.add_error('registration_no', 'You already have a car with that registration number')

    context = {
        'form': form,
        'registered_cars': registered_cars,
    }
    return render(request, 'placeholder/cars.html', context)


@login_required
def car_edit(request, car_id):
    success = None
    if request.method == 'POST':
        car = Car.objects.get(pk=car_id)
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = CarForm(instance=Car.objects.get(pk=car_id))

    context = {
        'form': form,
        'pk': car_id,
        'success': success,
    }

    template = 'placeholder/car-edit.html'
    return render(request, template, context)


@login_required
def car_delete(request, reg_no):
    try:
        car = Car.objects.get(user=request.user, registration_no=reg_no)
        mileage_instances = MilageInstance.objects.filter(user=request.user, car=car)
        car.delete()
        mileage_instances.delete()
        current_car = get_current_car(request) # will take care of session car etc.
    except ObjectDoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def change_car(request, reg_no):
    request.session['current_car'] = reg_no
    return redirect(request.META.get('HTTP_REFERER'))
