from django.contrib.auth.models import User
from django.urls import reverse, resolve
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from profiles.models import User, Page, Post


class PageApiUserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser1', password='qwspompumpopa25')

    def setUp(self):
        self.client.login(username='testuser1', password='qwspompumpopa25')

    def test_create_page(self):
        url = reverse('pages:pages-list')
        data = {'name': 'test', 'description': 'text', 'tags': []}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Page.objects.count(), 1)

        page = Page.objects.get()

        self.assertEqual(page.name, 'test')
        self.assertEqual(page.description, 'text')
        self.assertEqual(page.owner, self.user)

    def test_update_page(self):
        self.page = Page.objects.create(name='test', description='text', owner=self.user, image='image')
        url = reverse('pages:pages-detail', kwargs={'pk': self.page.pk})
        data = {'name': 'test1', 'description': 'text1'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        page = Page.objects.get()

        self.assertEqual(page.name, 'test1')
        self.assertEqual(page.description, 'text1')


class PostApiUserTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser1', password='qwspompumpopa25')

    def setUp(self):
        self.client.login(username='testuser1', password='qwspompumpopa25')
        self.page = Page.objects.create(name='test', description='text1', owner=self.user, image='image')

    def test_create_post(self):
        data = {'page_id': self.page.pk, 'page': self.page.pk, "content": 'topic', 'likes': self.user.username}
        url = reverse('posts:posts-list')

        with patch('profiles.post_views.send_email.delay') as mock_task:
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            mock_task.assert_called_once_with(self.page.pk)
