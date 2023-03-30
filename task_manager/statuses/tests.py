"""Statuses test module"""
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from task_manager.statuses.models import Status
from task_manager.users.models import User


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['statuses.json', 'users.json']

    def setUp(self):
        """Preparing models objects"""
        self.status1 = Status.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.status_creation_url = reverse('statuses:create')
        self.url_upd_status = reverse('statuses:upd_status', kwargs={'pk': 1})
        self.url_del_status = reverse('statuses:del_status', kwargs={'pk': 1})


class StatusesViewTest(SetUpTests):
    """Statuses view test"""

    def test_statuses_view(self):
        """Testing statuses main page"""
        url = reverse('statuses:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/statuses.html')
        self.assertContains(response, 'teststatus')
        self.assertContains(response, 'Test status 2')
        self.assertContains(response, 'Test status 3')


class StatusCreateViewTest(SetUpTests):
    """Test for status creation"""

    def test_status_creation_form_displayed(self):
        """Status creation form display test"""
        response = self.client.get(self.status_creation_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_status_created_successfully(self):
        """Status create test"""
        status_data = {'name': 'Test status'}
        response = self.client.post(self.status_creation_url, data=status_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Status.objects.count(), 4)
        self.assertEqual(Status.objects.last().name, 'Test status')


class StatusUpdateViewTestCase(SetUpTests):
    """Update status tests"""

    def test_unauthenticated_user_redirected_to_login(self):
        """No auth user"""
        self.client.logout()
        response = self.client.get(self.url_upd_status)

        self.assertRedirects(
            response,
            reverse('login'),
        )

    def test_authenticated_user_can_access_view(self):
        """Get access with auth user"""
        response = self.client.get(self.url_upd_status)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'form.html')

    def test_correct_status_displayed_on_form(self):
        """Test update form"""
        response = self.client.get(self.url_upd_status)
        form = response.context['form']

        self.assertEqual(form.instance, self.status1)

    def test_user_can_update_status_data(self):
        """Test update result"""
        data = {'name': 'Updated name'}
        response = self.client.post(self.url_upd_status, data=data)

        self.assertRedirects(response, reverse('statuses:index'))
        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, 'Updated name')

    def test_invalid_form_returns_form_with_errors(self):
        """Test update errors"""
        data = {'name': ''}
        response = self.client.post(self.url_upd_status, data)
        form = response.context['form']

        self.assertFalse(form.is_valid())


class TestDeleteViewTestCase(SetUpTests):
    """Delete statuses testing"""

    def test_redirect_if_not_logged_in(self):
        """Redirect to log in test"""
        self.client.logout()
        response = self.client.get(self.url_del_status)

        self.assertRedirects(
            response,
            reverse("login"),
        )

    def test_successful_status_deletion(self):
        """Status deletion test"""
        response = self.client.post(self.url_del_status)

        self.assertRedirects(response, reverse('statuses:index'))
        self.assertEqual(Status.objects.filter(id=self.status1.id).count(), 0)

    def test_correct_template_used(self):
        """Testing if correct template used"""
        response = self.client.get(self.url_del_status)

        self.assertTemplateUsed(response, 'statuses/status_delete.html')
