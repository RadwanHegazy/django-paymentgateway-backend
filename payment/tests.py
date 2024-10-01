from django.test import TestCase
from .models import Payment
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from django.urls import reverse
import uuid

class TestPaymentApp(TestCase) :

    def create_user(self) : 
        user = User.objects.create(
            full_name='test',
            email='test@gmail.com',
            password='test'
        )
        user.save()
        return user
    
    def create_headers (self,user=None) : 
        if user:
            tokens = AccessToken.for_user(user)
        else:
            tokens = AccessToken.for_user(self.create_user())
        return {
            'Authorization' : f"Bearer {tokens}"
        }
    
    def setUp(self) -> None:
        self.get_owner_payments = reverse('get_payments')
        self.create_owner_payment = reverse('owner_create_payment')

    def test_get_owner_payments_invalid (self) :
        response = self.client.get(self.get_owner_payments)
        self.assertNotEqual(response.status_code, 200)

    def test_get_owner_payments_valid (self) :
        response = self.client.get(self.get_owner_payments, headers=self.create_headers())
        self.assertEqual(response.status_code, 200)
    
    def test_get_undefined_payment_page(self) : 
        respone = self.client.get(
            reverse('get_payment', args=[str(uuid.uuid4())])
        )
        self.assertEqual(respone.status_code, 404)
    
    def test_get_defined_payemnt_page(self) :
        pay = Payment.objects.create(
            user=self.create_user(),
            amount=100
        ) 

        response = self.client.get(
            reverse('get_payment', args=[pay.id])
        )

        amount = response.json()['amount']
        self.assertEqual(amount, pay.amount)
        self.assertEqual(response.status_code, 200)

    def test_create_owner_payment_success (self):
        data = {
            'amount' : 200
        }
        user = self.create_user()
        response = self.client.post(
            reverse('owner_create_payment'),
            headers=self.create_headers(user),
            data=data
        )

        self.assertEqual(response.status_code, 201)

    def test_create_owner_payment_unauth (self):
        data = {
            'amount' : 200
        }
        response = self.client.post(
            reverse('owner_create_payment'),
            data=data
        )

        self.assertNotEqual(response.status_code, 201)

    def test_create_owner_payment_nodata (self):
        
        response = self.client.post(
            reverse('owner_create_payment'),
            headers=self.create_headers()
        )

        self.assertEqual(response.status_code, 400)

    def test_done_payment_success(self): 
        p = Payment.objects.create(
            user=self.create_user(),
            amount=100
        )
        p.save()
        data = {
                'card_cvc' : '123',
                'card_number' : 123456789123,
                'card_exp' : '02/30',
                'full_name' : 'Tester',
                'email' : "test@gmail.com"
            }
        response = self.client.post(
            reverse('create_payment', args=[p.id]),
            data=data
        )

        self.assertEqual(response.status_code, 200)

    def test_done_payment_no_data(self): 
        p = Payment.objects.create(
            user=self.create_user(),
            amount=100
        )
        p.save()
        response = self.client.post(
            reverse('create_payment', args=[p.id]),
            data={}
        )

        self.assertNotEqual(response.status_code, 200)


    def test_done_payment_invalid_id(self): 
        p = Payment.objects.create(
            user=self.create_user(),
            amount=100
        )
        p.save()
        data = {
                'card_cvc' : '123',
                'card_number' : 123456789123,
                'card_exp' : '02/30',
                'full_name' : 'Tester',
                'email' : "test@gmail.com"
            }
        response = self.client.post(
            reverse('create_payment', args=[str(uuid.uuid4())]),
            data=data
        )

        self.assertNotEqual(response.status_code, 200)
