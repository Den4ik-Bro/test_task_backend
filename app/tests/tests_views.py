from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Account, Session, Action
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

