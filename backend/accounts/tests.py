from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# Create your tests here.
class UserViewClass(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user = User.objects.create_user(email='test1@mail.ru', password='0910374adf')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_user(self):
        """
        Тест создания объекта User
        """

        url = reverse('user-list')
        data = {'email': 'mynew@email.ru', 'password': '643941ab'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 3)

        new_user = User.objects.get(email='mynew@email.ru')
        self.assertEqual(new_user.email, data['email'])
        self.assertTrue(check_password(data['password'], new_user.password))
        self.assertTrue(new_user.activation_key)

    def test_get_detail_user(self):
        """
        Тест запроса деталей об объекте User
        """
        url = reverse('user-detail', kwargs={'pk': self.user.pk})

        non_auth_response = self.client.get(url)
        self.assertEqual(non_auth_response.status_code, status.HTTP_401_UNAUTHORIZED)

        auth_response = self.client.get(url, headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(auth_response.data), 3)
        self.assertEqual(auth_response.data['email'], self.user.email)
        self.assertEqual(auth_response.data['activation_key'], str(self.user.activation_key))

    def test_change_password(self):
        url = reverse('user-change-password', kwargs={'pk': self.user.pk})
        incorrect_data1 = {'old_password': '0910374adf', 'new_password': '045402'}
        incorrect_data2 = {'old_password': '723747gfegh', 'new_password': '89348248jgfhd'}
        correct_data = {'old_password': '0910374adf', 'new_password': '89348248jgfhd'}

        non_auth_response = self.client.patch(url, correct_data, format='json')
        self.assertEqual(non_auth_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.user.refresh_from_db()
        self.assertFalse(check_password('643941ab', self.user.password))

        auth_bad_response1 = self.client.patch(url, incorrect_data1,
                                               headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(auth_bad_response1.status_code, status.HTTP_400_BAD_REQUEST)

        auth_bad_response2 = self.client.patch(url, incorrect_data2,
                                               headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(auth_bad_response2.status_code, status.HTTP_400_BAD_REQUEST)

        auth_response = self.client.patch(url, correct_data, format='json',
                                          headers={'Authorization': f'Bearer {self.access_token}'})
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(auth_response.data), 1)
        self.user.refresh_from_db()
        self.assertTrue(check_password(correct_data['new_password'], self.user.password))

    def test_update_key(self):
        url = reverse('user-update-key', kwargs={'pk': self.user.pk})

        non_auth_response = self.client.patch(url)
        self.assertEqual(non_auth_response.status_code, 401)
        self.assertNotIn('activation_key', non_auth_response.data)

        auth_response = self.client.patch(url, headers={'Authorization': f'Bearer {self.access_token}'})
        self.user.refresh_from_db()
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(auth_response.data), 1)
        self.assertIn('activation_key', auth_response.data)
        self.assertEqual(self.user.activation_key, str(auth_response.data['activation_key']))
