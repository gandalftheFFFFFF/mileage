from django.test import TestCase
from .models import MilageInstance

# Create your tests here.
class AmountPerLiterTestCase(TestCase):
    def setUp(self):
        MilageInstance.objects.create(date='1/1/1970', km_stand=0)
        MilageInstance.objects.create

    def test_amount_per_liter(self):
        pass