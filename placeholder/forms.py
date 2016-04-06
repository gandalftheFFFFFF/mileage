from placeholder.models import Car
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['car'] = forms.ModelChoiceField(queryset=Car.objects.filter(user=user))
        self.fields['car'].empty_label = None