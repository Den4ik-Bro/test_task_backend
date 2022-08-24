import datetime

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Account, Session, Action, Accrual, Payment
from django.utils import timezone


class AccountViewSetTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create(number=1, name='Жора')
        session = Session.objects.create(
            account=account,
            created_at=timezone.now(),
            session_id='qwerty'
        )

        CHOICES = ['чтение', 'создание', 'изменение', 'удаление']
        actions = [
            Action(session=session, type=action, created_at=timezone.now()) for action in CHOICES
        ]
        Action.objects.bulk_create(actions)

    def test_list_method(self):
        url = reverse('app:account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Account.objects.count())

    def test_retrieve_method(self):
        account = Account.objects.first()
        url = reverse('app:account-detail', kwargs={'pk': account.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], account.name)
        self.assertEqual(response.data['number'], account.number)

    def test_account_actions_method(self):
        account = Account.objects.first()
        url = reverse('app:account-account-actions', kwargs={'pk': account.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['number'], account.number)
        self.assertEqual(len(response.data['result']['action']), 4)
        self.assertEqual(response.data['result']['action'][0]['count'], 1)


class AccrualViewTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        accruals = [Accrual(date=datetime.datetime(2022, num, num)) for num in range(1, 13)]
        Accrual.objects.bulk_create(accruals)
        payments = [Payment(date=datetime.datetime(2022, num, num + 3)) for num in range(1, 13)]
        Payment.objects.bulk_create(payments)
        Payment.objects.create(date=datetime.datetime(2022, 1, 20))

    def test_get_method(self):
        url = reverse('app:accrual')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 13)
        self.assertEqual(response.data['платеж 2022-01-04 id 1'], 'долг 2022-01-01 id 1')
        self.assertEqual(response.data['платеж 2022-01-20 id 13'], 'нет долга для этого платежа')



