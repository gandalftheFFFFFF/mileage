__author__ = 'niels'

from django import forms


class MilageForm(forms.Form):
    date = forms.DateField(label='Date')
    km = forms.CharField(label='Km', widget=forms.NumberInput)
    amount = forms.DecimalField(label='Amount')
    liter = forms.DecimalField(label='Liter')


DATE_CHOICES = [
    ('dd/mm/yyyy','dd/mm/yyyy'),
    ('mm/dd/yyyy','mm/dd/yyyy'),
    ('yyyy/mm/dd','yyyy/mm/dd'),
    ('yyyy/dd/mm','yyyy/dd/mm')
]

CURRENCY_CHOICES = [
    'DKK',
    'USD'
]

VOLUME_CHOICES = [
    'Liter',
    'US gallons'
]


class UploadFileForm(forms.Form):
    file = forms.FileField()
    date_format = forms.ChoiceField(choices=DATE_CHOICES)