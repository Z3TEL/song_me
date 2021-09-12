from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from .models import *

User = get_user_model()


class TestAuthor(TestCase):
    def setUp(self)-> None:
        self.user = User.objects.create_user('test32@mail.com',
                                             '1234',
                                             name='User1',
                                             is_active=True)
        self.admin = User.objects.create_superuser('admin@gmail.com',
                                                   '1234',
                                                   name='Admin1')
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

        self.author1 = Author.objects.create(name='author1')
        self.author2 = Author.objects.create(name='author2')

        self.author_payload = {
            'name': 'Test',
        }

    def artist_test_list(self):
        client = APIClient()
        url = reverse('author-list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_artist_as_anonymous_user(self):
        client = APIClient()
        url = reverse('author-list')
        response = client.post(url, data=self.author_payload)
        self.assertEqual(response.status_code, 401)

    def test_create_artist_as_regular_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        url = reverse('author-list')
        response = client.post(url, data=self.author_payload)
        self.assertEqual(response.status_code, 403)

    def test_create_artist_as_admin_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('author-list')
        response = client.post(url, data=self.author_payload)
        self.assertEqual(response.status_code, 201)

    def test_create_artist_without_name(self):
        data = self.author_payload.copy()
        data.pop('name')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('author-list')
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)

    def genre_test_delete(self):
        author1_id = self.author1.id
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('author-detail', args=(author1_id,))
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIs(response.data, None)


class TestGenre(TestCase):
    def setUp(self)-> None:
        self.user = User.objects.create_user('test32@mail.com',
                                             '1234',
                                             name='User1',
                                             is_active=True)
        self.admin = User.objects.create_superuser('admin@gmail.com',
                                                   '1234',
                                                   name='Admin1')
        self.user_token = Token.objects.create(user=self.user)
        self.admin_token = Token.objects.create(user=self.admin)

        self.genre1 = Genre.objects.create(slug='rap', name='Rap')
        self.genre2 = Genre.objects.create(slug='rock', name='Rock')
        self.genre3 = Genre.objects.create(slug='metal', name='Metal')
        self.genre4 = Genre.objects.create(slug='phonk', name='Phonk')

        self.genre_payload = {
            'slug': 'lo-fi',
            'name': 'Lo-Fi',
        }

    def genre_test_list(self):
        client = APIClient()
        url = reverse('genre-list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 4)

    def test_create_genre_as_anonymous_user(self):
        client = APIClient()
        url = reverse('genre-list')
        response = client.post(url, data=self.genre_payload)
        self.assertEqual(response.status_code, 401)

    def test_create_genre_as_regular_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        url = reverse('genre-list')
        response = client.post(url, data=self.genre_payload)
        self.assertEqual(response.status_code, 403)

    def test_create_genre_as_admin_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('genre-list')
        response = client.post(url, data=self.genre_payload)
        self.assertEqual(response.status_code, 201)

    def test_create_genre_without_name(self):
        data = self.genre_payload.copy()
        data.pop('name')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('genre-list')
        response = client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)

    def genre_test_delete(self):
        genre1_id = self.genre1.id
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        url = reverse('genre-detail', args=(genre1_id,))
        response = client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIs(response.data, None)



# TODO: починить тесты на песни


# class TestSong(TestCase):
#     def setUp(self)-> None:
#         self.user = User.objects.create_user('test32@mail.com',
#                                              '1234',
#                                              name='User1',
#                                              is_active=True)
#         self.admin = User.objects.create_superuser('admin@gmail.com',
#                                                    '1234',
#                                                    name='Admin1')
#         self.user_token = Token.objects.create(user=self.user)
#         self.admin_token = Token.objects.create(user=self.admin)
#
#         self.author1 = Author.objects.create(name='author1')
#         self.author2 = Author.objects.create(name='author2')
#
#         self.genre1 = Genre.objects.create(slug='rap', name='Rap')
#         self.genre2 = Genre.objects.create(slug='rock', name='Rock')
#         self.genre3 = Genre.objects.create(slug='metal', name='Metal')
#         self.genre4 = Genre.objects.create(slug='phonk', name='Phonk')
#
#         self.song1 = Song.objects.create(title='Test1', artist=self.author1, genre=self.genre1, duration='2:30')
#         self.song2 = Song.objects.create(title='Test2', artist=self.author2, genre=self.genre2, duration='2:30')
#
#         self.song_payload = {
#             'title': 'test3',
#             'artist': self.author1.id,
#             'genre': self.genre3.set,
#             'duration': '2:30'
#         }
#
#     def test_list(self):
#         client = APIClient()
#         url = reverse('product-list')
#         response = client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data['results']), 4)
