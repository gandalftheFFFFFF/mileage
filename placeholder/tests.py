from django.test import TestCase
from .models import MilageInstance
from django.contrib.auth.models import User

# Create your tests here.
class AmountPerLiterTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='u1')
        u1 = User.objects.get(username='u1')
        MilageInstance.objects.create(date='1970-01-01', km_stand=0, amount=100, liter=10, user=u1)
        MilageInstance.objects.create(date='1971-01-01', km_stand=100, amount=100, liter=10, user=u1)
        MilageInstance.objects.create(date='1972-01-01', km_stand=400, amount=100, liter=10, user=u1)

    def test_amount_per_liter(self):
        m1 = MilageInstance.objects.get(km_stand=0)
        m2 = MilageInstance.objects.get(km_stand=100)
        m3 = MilageInstance.objects.get(km_stand=400)
        self.assertEqual(m2.trip(), m2.km_stand-m1.km_stand)
        self.assertEqual(m3.trip(), m3.km_stand-m2.km_stand)