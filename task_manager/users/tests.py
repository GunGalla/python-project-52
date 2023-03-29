"""Tasks test module"""
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['users.json']

    def setUp(self):
        """Preparing models objects"""
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user1.set_password('testpass')
        self.user1.save()
        self.user_creation_url = reverse('users:create')
        self.url_upd_user = reverse('users:upd_user', kwargs={'pk': 1})
        self.url_del_user = reverse('users:del_user', kwargs={'pk': 1})
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
                'Note that both fields may be case-sensitive.'),
        )


class LogoutViewTestCase(SetUpTests):
    """Test for logout"""

    def test_logout(self):
        """Testing logout function"""
        self.client.force_login(self.user1)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.index_url)


class UsersViewTest(SetUpTests):
    """Users view test"""

    def test_users_view(self):
        """Testing users main page"""
        url = reverse('users:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/users.html')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'testuser2')
        self.assertContains(response, 'testuser3')


class UserCreateViewTest(SetUpTests):
    """Test for user creation"""

    def test_user_creation_form_displayed(self):
        """User creation form display test"""
        response = self.client.get(self.user_creation_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_create.html')

    def test_user_created_successfully(self):
        """User create test"""
        user_data = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser4',
            'password1': 'testpass',
            'password2': 'testpass',
        }
        response = self.client.post(self.user_creation_url, data=user_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.last().username, 'testuser4')


class UserUpdateViewTestCase(SetUpTests):
    """Update user tests"""

    def test_unauthenticated_user_redirected_to_login(self):
        """No auth user"""
        response = self.client.get(self.url_upd_user)

        self.assertRedirects(
            response,
            reverse('login'),
        )

    def test_correct_user_displayed_on_form(self):
        """Test update form"""
        self.client.force_login(self.user1)
        response = self.client.get(self.url_upd_user)
        form = response.context['form']

        self.assertEqual(form.instance, self.user1)

    def test_user_can_update_user_data(self):
        """Test user update result"""
        self.client.force_login(self.user1)
        data = {
            'first_name': 'Updated name',
            'last_name': 'Updated surname',
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass',
        }
        response = self.client.post(self.url_upd_user, data=data)

        self.assertRedirects(response, reverse('users:index'))
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'Updated name')
        self.assertEqual(self.user1.last_name, 'Updated surname')

    def test_invalid_form_returns_form_with_errors(self):
        """Test update errors"""
        self.client.force_login(self.user1)
        data = {'name': '', 'first_name': 'Updated name'}
        response = self.client.post(self.url_upd_user, data)
        form = response.context['form']

        self.assertFalse(form.is_valid())


class TestDeleteViewTestCase(SetUpTests):
    """Delete users testing"""

    def test_redirect_if_not_logged_in(self):
        """Redirect to log in test"""
        response = self.client.get(self.url_del_user)

        self.assertRedirects(
            response,
            reverse("login"),
        )

    def test_only_user_can_delete_himself(self):
        """User deletion test"""
        self.client.force_login(self.user2)
        response = self.client.get(self.url_del_user)

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_successful_user_deletion(self):
        """User deletion success test"""
        self.client.force_login(self.user2)
        response = self.client.post(reverse('users:del_user', kwargs={'pk': 2}))

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(User.objects.filter(id=self.user2.id).count(), 0)

    def test_correct_template_used(self):
        """Testing if correct template used"""
        self.client.force_login(self.user1)
        response = self.client.get(self.url_del_user)

        self.assertTemplateUsed(response, 'users/user_delete.html')
