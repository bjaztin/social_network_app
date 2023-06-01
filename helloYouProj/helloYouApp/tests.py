from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Post
from django.utils import timezone
from django.db.models import Count

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from helloYouApp.api.serializers import ProfileSerializer


class LoginTestCase(TestCase):

    def test_url_exists(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authenticate/login.html')


class ViewProfilesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
    )

    def test_url_exists(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('view_all_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('view_all_profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'main/all_profiles.html')


class PostViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
    )

    def test_url_exists(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('view_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('view_posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'main/posts.html')

class InvitationViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
    )

    def test_url_exists(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('view_invites')
        response = self.client.get(url)
        self.assertEqual(response.status_code,  status.HTTP_200_OK)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('view_invites'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'main/myInvitations.html')     