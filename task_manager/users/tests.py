"""Tasks test module"""
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from task_manager.users.models import User


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['users.json']

    def setUp(self):
        """Preparing models objects"""
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.user_creation_url = reverse('users:create')
        self.url_upd_user = reverse('users:upd_user', kwargs={'id': 1})
        self.url_del_user = reverse('users:del_user', kwargs={'id': 1})


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
        self.client.logout()
        response = self.client.get(self.user_creation_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_create.html')

    def test_user_created_successfully(self):
        """User create test"""
        self.client.logout()
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
        self.client.logout()
        response = self.client.get(self.url_upd_user)

        self.assertRedirects(
            response,
            reverse('login'),
        )

    def test_correct_user_displayed_on_form(self):
        """Test update form"""
        response = self.client.get(self.url_upd_user)
        form = response.context['form']

        self.assertEqual(form.instance, self.user1)

    def test_user_can_update_user_data(self):
        """Test user update result"""
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
        data = {'name': '', 'first_name': 'Updated name'}
        response = self.client.post(self.url_upd_user, data)
        form = response.context['form']

        self.assertFalse(form.is_valid())


class TestDeleteViewTestCase(SetUpTests):
    """Delete users testing"""

    def test_redirect_if_not_logged_in(self):
        """Redirect to log in test"""
        self.client.logout()
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
        response = self.client.post(reverse('users:del_user', kwargs={'id': 2}))

        self.assertRedirects(response, reverse('users:index'))
        self.assertEqual(User.objects.filter(id=self.user2.id).count(), 0)

    def test_correct_template_used(self):
        """Testing if correct template used"""
        response = self.client.get(self.url_del_user)

        self.assertTemplateUsed(response, 'users/user_delete.html')
