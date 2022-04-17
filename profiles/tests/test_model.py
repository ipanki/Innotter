from django.contrib.auth.models import User
from django.test import TestCase

from profiles.models import User, Page, Post


class PageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.user.save()

    def test_create_page(self):
        page = Page.objects.create(name='test', description='text', owner=self.user, image='image')
        page.save()
        self.assertEqual(page.name, 'test')
        self.assertEqual(page.description, 'text')
        self.assertEqual(page.owner, self.user)
        self.assertEqual(page.image, 'image')

    def test_create_post(self):
        page = Page.objects.create(name='test', description='text', owner=self.user, image='image')
        page.save()
        post = Post.objects.create(page=page, content='text')
        post.save()
        self.assertEqual(post.page, page)
        self.assertEqual(post.content, 'text')
