from django.db import models
from django.forms import ModelForm, forms
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

FUEL_TYPES = (
    ('DIESEL', 'Diesel'),
    ('PETROL', 'Petrol'),
    ('ELECTRICITY', 'Electricity'),
)


class Car(models.Model):
    registration_no = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPES, default='PETROL')
    date = models.DateField(verbose_name='Date (yyyy-mm-dd):')
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return 'Reg.no.: {}'.format(self.registration_no)

    class Meta:
        unique_together = ('registration_no', 'user')
        ordering = ['-date']


class CarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Car
        fields = ['registration_no', 'price', 'date', 'fuel_type', 'text', ]


class Expense(models.Model):
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    text = models.CharField(max_length=300)
    comment = models.TextField(null=True, blank=True)
    car = models.ForeignKey(Car)


class ExpenseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = Expense
        fields = ['amount', 'text', 'comment', 'car']


class MilageInstance(models.Model):
    date = models.DateTimeField(
        default=timezone.now(),
        verbose_name='Date (yyyy-mm-dd):',
    )
    km_stand = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Km driven')
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Fuel cost')
    liter = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Fuel volume')
    user = models.ForeignKey(User)
    car = models.ForeignKey(Car)

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return '{}: Km: {}, fuel cost: {}, fuel volume: {}'.format(self.date, self.km_stand, self.amount, self.liter)

    def km_pr_liter(self):
        if self.trip() == 0:
            return 0
        return self.trip() / self.liter

    def amount_pr_liter(self):
        if self.amount == 0:
            return 0
        elif self.liter == 0:
            return 0
        return self.amount / self.liter

    def trip(self):
        try:
            last_instance = MilageInstance.objects.all().filter(
                date__lte=self.date
            ).filter(
                user=self.user
            ).exclude(
                pk=self.pk
            ).order_by('-date')[0]
        except:
            return 0

        trip = self.km_stand - last_instance.km_stand
        print('self: {}, last: {}'.format(self.km_stand, last_instance.km_stand))
        return trip

    @classmethod
    def create(cls, date, km_stand, amount, liter, user, car):
        instance = cls(date=date, km_stand=km_stand, amount=amount, liter=liter, user=user, car=car)
        return instance


class MilageForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(MilageForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['car'].queryset = Car.objects.filter(user=user)
        self.fields['car'].empty_label = None

    class Meta:
        model = MilageInstance
        fields = ['date', 'km_stand', 'amount', 'liter', 'car']
