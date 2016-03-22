from django.db import models
from django.forms import ModelForm, forms
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class MilageInstance(models.Model):
    date = models.DateField(
        default=datetime.now(),
        verbose_name='Dato (yyyy-mm-dd):',
    )
    km_stand = models.DecimalField(max_digits=18, decimal_places=2)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    liter = models.DecimalField(max_digits=18, decimal_places=2)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return '{}: Km-stand: {}, Amount: {}, Liter: {}'.format(self.date, self.km_stand, self.amount, self.liter)

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
            last_instance = MilageInstance.objects.filter(
                date__lt=self.date
            ).filter(
                user=self.user
            ).order_by('-date')[0]
        except:
            return 0
        trip = self.km_stand - last_instance.km_stand
        return trip

    @classmethod
    def create(cls, date, km_stand, amount, liter, user):
        instance = cls(date=date, km_stand=km_stand, amount=amount, liter=liter, user=user)
        return instance


class MilageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MilageForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta:
        model = MilageInstance
        fields = ['date', 'km_stand', 'amount', 'liter', ]
