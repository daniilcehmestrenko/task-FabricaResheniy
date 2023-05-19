from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import MailingList, Client


class MailingListTests(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'dttm_start': timezone.now(),
            'text': 'Hello!',
            'client_filter': 'test',
            'dttm_end': timezone.now() + timezone.timedelta(hours=1)
        }
        self.new_data = {
            'text': 'New Hello',
            'client_filter': 'New filter'
        }

    def create_mailinglist(self):
        return MailingList.objects.create(**self.data)

    def test_create_mailinglist(self):
        url = reverse('mailinglist-list')
        response = self.client.post(url, self.data, format='json')
        data = response.json()
        mailinglist = MailingList.objects.filter(pk=data['id']).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(mailinglist)
        self.assertEqual(mailinglist.dttm_start, self.data['dttm_start'])
        self.assertEqual(mailinglist.text, self.data['text'])
        self.assertEqual(mailinglist.client_filter, self.data['client_filter'])
        self.assertEqual(mailinglist.dttm_end, self.data['dttm_end'])

    def test_get_mailinglist(self):
        mailinglist = self.create_mailinglist()
        url = reverse('mailinglist-list')
        response = self.client.get(url)
        data = response.json()
        count_mailinglist = MailingList.objects.all().count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(data), list)
        self.assertEqual(len(data), count_mailinglist)
        self.assertEqual(mailinglist.pk, data[-1]['id'])
        self.assertEqual(mailinglist.text, data[-1]['text'])
        self.assertEqual(mailinglist.client_filter, data[-1]['client_filter'])

    def test_update_mailinglist(self):
        mailinglist = self.create_mailinglist()
        url = reverse('mailinglist-detail', kwargs={'pk': mailinglist.pk})
        response = self.client.patch(url, self.new_data)
        data = response.json()
        up_mailinglist = MailingList.objects.filter(pk=mailinglist.pk).first()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(up_mailinglist)
        self.assertEqual(up_mailinglist.text, data['text'])
        self.assertEqual(up_mailinglist.client_filter, data['client_filter'])

    def test_get_detail_mailinglist(self):
        mailinglist = self.create_mailinglist()
        url = reverse('mailinglist-detail', kwargs={'pk': mailinglist.pk})
        response = self.client.get(url, self.new_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mailinglist.pk, data['id'])
        self.assertEqual(mailinglist.text, data['text'])
        self.assertEqual(mailinglist.client_filter, data['client_filter'])


class ClientTests(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'phone': '79173333333',
            'code': '917',
            'tag': '#mts',
            'timezone': 'UCT00:00'
        }
        self.new_data = {
            'phone': '79274444444',
            'code': '927',
            'tag': '#megafon',
        }

    def create_client(self):
        return Client.objects.create(**self.data)

    def test_get_client_list(self):
        client = self.create_client()
        url = reverse('client-list')
        response = self.client.get(url)
        data = response.json()
        count_client = Client.objects.all().count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(data), list)
        self.assertEqual(len(data), count_client)
        self.assertEqual(client.phone, data[-1]['phone'])
        self.assertEqual(client.code, data[-1]['code'])
        self.assertEqual(client.tag, data[-1]['tag'])
        self.assertEqual(client.timezone, data[-1]['timezone'])

    def test_create_client(self):
        url = reverse('client-list')
        response = self.client.post(url, self.data)
        data = response.json()
        client = Client.objects.filter(pk=data['id']).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(client)
        self.assertEqual(client.phone, data['phone'])
        self.assertEqual(client.code, data['code'])
        self.assertEqual(client.tag, data['tag'])
        self.assertEqual(client.timezone, data['timezone'])

    def test_update_client(self):
        client = self.create_client()
        url = reverse('client-detail', kwargs={'pk': client.pk})
        response = self.client.patch(url, self.new_data)
        data = response.json()
        up_client = Client.objects.filter(pk=client.pk).first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(up_client)
        self.assertEqual(up_client.phone, data['phone'])
        self.assertEqual(up_client.code, data['code'])
        self.assertEqual(up_client.tag, data['tag'])

    def test_get_detail_client(self):
        client = self.create_client()
        url = reverse('client-detail', kwargs={'pk': client.pk})
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(client.pk, data['id'])
        self.assertEqual(client.phone, data['phone'])
        self.assertEqual(client.code, data['code'])
        self.assertEqual(client.tag, data['tag'])
        self.assertEqual(client.timezone, data['timezone'])