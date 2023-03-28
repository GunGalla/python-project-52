"""Tasks test module"""
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User


class SetUpTests(TestCase):
    """Enabling fixtures"""
    fixtures = ['tasks.json', 'statuses.json', 'users.json']

    def setUp(self):
        """Preparing models objects"""
        self.task1 = Task.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.task_creation_url = reverse('tasks:create')
        self.url_upd_task = reverse('tasks:upd_tasks', kwargs={'pk': 1})
        self.url_del_task = reverse('tasks:del_tasks', kwargs={'pk': 1})


class TasksViewTest(SetUpTests):
    """Tasks view test"""

    def test_tasks_view(self):
        """Testing tasks main page"""
        url = reverse('tasks:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/tasks.html')
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')


class TaskViewTest(SetUpTests):
    """Distinct task page test"""

    def test_task_view(self):
        """Testing distinct task page"""
        url = reverse('tasks:task', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task.html')
        self.assertContains(response, 'Task 1')


class TaskCreateViewTest(SetUpTests):
    """Test for task creation"""

    def test_task_creation_form_displayed(self):
        """Task creation form display test"""
        response = self.client.get(self.task_creation_url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_create.html')

    def test_task_created_successfully(self):
        """Task create test"""
        task_data = {
            'name': 'Test Task',
            'status': self.status1.id,
        }
        response = self.client.post(self.task_creation_url, data=task_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(Task.objects.last().name, 'Test Task')


class TaskUpdateViewTestCase(SetUpTests):
    """Update task tests"""

    def test_unauthenticated_user_redirected_to_login(self):
        """No auth user"""
        self.client.logout()
        response = self.client.get(self.url_upd_task)

        self.assertRedirects(
            response,
            reverse('login') + '?next=' + self.url_upd_task,
        )

    def test_authenticated_user_can_access_view(self):
        """Get access with auth user"""
        response = self.client.get(self.url_upd_task)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_update.html')

    def test_correct_task_displayed_on_form(self):
        """Test update form"""
        response = self.client.get(self.url_upd_task)
        form = response.context['form']

        self.assertEqual(form.instance, self.task1)

    def test_user_can_update_task_data(self):
        """Test update result"""
        data = {
            'name': 'Updated name',
            'description': 'Updated description',
            'status': self.status1.id,
        }
        response = self.client.post(self.url_upd_task, data=data)

        self.assertRedirects(response, reverse('tasks:index'))
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, 'Updated name')
        self.assertEqual(self.task1.description, 'Updated description')

    def test_invalid_form_returns_form_with_errors(self):
        """Test update errors"""
        data = {'name': '', 'status': self.status1.id}
        response = self.client.post(self.url_upd_task, data)
        form = response.context['form']

        self.assertFalse(form.is_valid())


class TestDeleteViewTestCase(SetUpTests):
    """Delete tasks testing"""

    def test_redirect_if_not_logged_in(self):
        """Redirect to log in test"""
        self.client.logout()
        response = self.client.get(self.url_del_task)

        self.assertRedirects(
            response,
            f'{reverse("login")}?next={self.url_del_task}'
        )

    def test_only_author_can_delete_task(self):
        """Author task deletion test"""
        self.client.force_login(self.user2)
        response = self.client.get(self.url_del_task)

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_successful_task_deletion(self):
        """Task deletion test"""
        response = self.client.post(self.url_del_task)

        self.assertRedirects(response, reverse('tasks:index'))
        self.assertEqual(Task.objects.filter(id=self.task1.id).count(), 0)

    def test_correct_template_used(self):
        """Testing if correct template used"""
        self.client.force_login(self.user1)
        response = self.client.get(self.url_del_task)

        self.assertTemplateUsed(response, 'tasks/task_delete.html')
