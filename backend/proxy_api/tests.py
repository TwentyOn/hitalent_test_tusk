from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import VirtualMachine


# Create your tests here.
class ActivateKeyViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vm1 = VirtualMachine.objects.create(name='proxy1', host='203.236.197.76', port=8080, protocol='http')
        self.vm2 = VirtualMachine.objects.create(name='proxy2', host='186.174.48.132', port=8080, protocol='https')
        self.vm3 = VirtualMachine.objects.create(name='proxy3', host='209.191.114.209', port=8080, protocol='socks5')
        self.user = get_user_model().objects.create(email='test@mail.ru', password='09testpassword')

    def test_activate_key(self):
        """
        Тест активации ключа и закрепления пользователя за VM
        """

        url = reverse('activate-key')

        activation_key = self.user.activation_key
        data = {'activation_key': activation_key}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.activation_key, activation_key)

        cur_vm = VirtualMachine.objects.filter(current_user=self.user)
        self.assertEqual(cur_vm.exists(), True)
        self.assertEqual(cur_vm[0].host, response.data['host'])
        self.assertEqual(cur_vm[0].port, response.data['port'])
        self.assertEqual(cur_vm[0].protocol, response.data['protocol'])
        self.assertEqual(
            VirtualMachine.objects.
            exclude(id=cur_vm[0].id).
            filter(current_user=self.user).
            exists(), False)
