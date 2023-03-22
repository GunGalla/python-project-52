"""Labels test module"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from http import HTTPStatus

from labels.models import Label


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['labels.json', 'users.json']

    def setUp(self):
        """Preparing models objects"""
        self.label1 = Label.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.label_creation_url = reverse('labels:create')
        self.url_upd_label = reverse('labels:upd_label', kwargs={'id': 1})
        self.url_del_label = reverse('labels:del_label', kwargs={'id': 1})


class LabelsViewTest(SetUpTests):
    """Labels view test"""

    def test_labels_view(self):
        """Testing labels main page"""
        url = reverse('labels:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/labels.html')
        self.assertContains(response, 'Test label 1')
        self.assertContains(response, 'Test label 2')
        self.assertContains(response, 'Test label 3')


class LabelCreateViewTest(SetUpTests):
    """Test for label creation"""

    def test_label_creation_form_displayed(self):
        """Label creation form display test"""
        response = self.client.get(self.label_creation_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_create.html')

    def test_label_created_successfully(self):
        """Label create test"""
        label_data = {'name': 'Test label'}
        response = self.client.post(self.label_creation_url, data=label_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Label.objects.count(), 4)
        self.assertEqual(Label.objects.last().name, 'Test label')


class LabelUpdateViewTestCase(SetUpTests):
    """Update label tests"""

    def test_unauthenticated_user_redirected_to_login(self):
        """No auth user"""
        self.client.logout()
        response = self.client.get(self.url_upd_label)

        self.assertRedirects(
            response,
            reverse('login') + '?next=' + self.url_upd_label,
        )

    def test_authenticated_user_can_access_view(self):
        """Get access with auth user"""
        response = self.client.get(self.url_upd_label)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_update.html')

    def test_correct_label_displayed_on_form(self):
        """Test update form"""
        response = self.client.get(self.url_upd_label)
        form = response.context['form']

        self.assertEqual(form.instance, self.label1)

    def test_user_can_update_label_data(self):
        """Test update result"""
        data = {'name': 'Updated name'}
        response = self.client.post(self.url_upd_label, data=data)

        self.assertRedirects(response, reverse('labels:index'))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'Updated name')

    def test_invalid_form_returns_form_with_errors(self):
        """Test update errors"""
        data = {'name': ''}
        response = self.client.post(self.url_upd_label, data)
        form = response.context['form']

        self.assertFalse(form.is_valid())


class TestDeleteViewTestCase(SetUpTests):
    """Delete labels testing"""

    def test_redirect_if_not_logged_in(self):
        """Redirect to log in test"""
        self.client.logout()
        response = self.client.get(self.url_del_label)

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={self.url_del_label}'
        )

    def test_successful_label_deletion(self):
        """Label deletion test"""
        response = self.client.post(self.url_del_label)

        self.assertRedirects(response, reverse('labels:index'))
        self.assertEqual(Label.objects.filter(id=self.label1.id).count(), 0)

    def test_correct_template_used(self):
        """Testing if correct template used"""
        response = self.client.get(self.url_del_label)

        self.assertTemplateUsed(response, 'labels/label_delete.html')
