"""Tasks test module"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from http import HTTPStatus
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['users.json']

    def setUp(self):
        """Preparing models objects"""
        self.user1 = User.objects.get(pk=1)
        self.user1.set_password('testpass')
        self.user1.save()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.index_url = reverse('index')


class IndexViewTestCase(SetUpTests):
    """Tasks view test"""

    def test_index_view(self):
        """Testing tasks main page"""
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')


class LoginViewTestCase(SetUpTests):
    """Login page test"""

    def test_get_login_page(self):
        """Test getting login page"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')

    def test_post_with_valid_credentials(self):
        """Test successful login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser', 'password': 'testpass'
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), _('You logged in'))

    def test_post_with_invalid_credentials(self):
        """Test login failure"""
        response = self.client.post(self.login_url, {
            'username': 'testuser', 'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertNotIn('_auth_user_id', self.client.session)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            _('Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.')
        )


class LogoutViewTestCase(SetUpTests):
    """Test for logout"""

    def test_logout(self):
        """Testing logout function"""
        self.client.force_login(self.user1)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.index_url)
