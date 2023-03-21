from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from django.contrib.auth.models import User
from .models import UserProfile, Project, Timelog
from .serializers import ProjectSerializer, TimelogSerializer

class TimelogViewTestCase(APITestCase):
    client = APIClient()
    username = 'testuser'
    password = 'testpass123'

    def setUp(self):
        User.objects.create(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        self.project = Project.objects.create(
            project_id='PROJ001',
            project_name='Test Project'
        )
        self.user_profile = UserProfile.objects.create(
            user=User.objects.get(username=self.username),
            project=self.project
        )

    def test_get_timelogs(self):
        url = reverse('timelogs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_timelog(self):
        url = reverse('timelogs')
        data = {
            "user": User.objects.get(username=self.username).id,
            "project": self.project.id,
            "date": "2021-10-28",
            "time_logged": "2.5",
            "description": "Test Timelog"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_timelog_unauthorized_user(self):
        url = reverse('timelogs')
        data = {
            "user": User.objects.create(username='unauthorizeduser', password='testpass123').id,
            "project": self.project.id,
            "date": "2021-10-28",
            "time_logged": "2.5",
            "description": "Test Timelog"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_add_timelog_for_unallocated_project(self):
        url = reverse('timelogs')
        project = Project.objects.create(
            project_id='PROJ002',
            project_name='Test Project 2'
        )
        data = {
            "user": User.objects.get(username=self.username).id,
            "project": project.id,
            "date": "2021-10-28",
            "time_logged": "2.5",
            "description": "Test Timelog"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
class TimelogDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.project = Project.objects.create(
            project_id='test_project', project_name='Test Project'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user, project=self.project
        )
        self.timelog = Timelog.objects.create(
            user=self.user, project=self.project, hours=5.5, notes='test note'
        )

    def test_edit_timelog(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        data = {
            'user': self.user.id,
            'project': self.project.id,
            'hours': 7.5,
            'notes': 'updated note',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.timelog.refresh_from_db()
        serializer = TimelogSerializer(self.timelog)
        self.assertEqual(response.data, serializer.data)

    def test_edit_timelog_for_another_user(self):
        user2 = User.objects.create_user(
            username='testuser2', password='testpass'
        )
        self.client.login(username='testuser2', password='testpass')
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        data = {
            'user': self.user.id,
            'project': self.project.id,
            'hours': 7.5,
            'notes': 'updated note',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_edit_timelog_for_different_project(self):
        project2 = Project.objects.create(
            project_id='test_project2', project_name='Test Project 2'
        )
        self.client.login(username='testuser', password='testpass')
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        data = {
            'user': self.user.id,
            'project': project2.id,
            'hours': 7.5,
            'notes': 'updated note',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

class TimelogDetailDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client.force_login(self.user)
        self.project = Project.objects.create(
            project_id='123', project_name='Test Project')
        self.timelog = Timelog.objects.create(
            user=self.user, project=self.project, hours=5)

    def test_delete_timelog(self):
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Timelog.objects.filter(id=self.timelog.id).exists())

    def test_delete_timelog_unauthenticated(self):
        self.client.logout()
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Timelog.objects.filter(id=self.timelog.id).exists())

    def test_delete_timelog_forbidden(self):
        user2 = User.objects.create_user(
            username='testuser2', password='testpass2')
        self.client.force_login(user2)
        url = reverse('timelog-detail', kwargs={'pk': self.timelog.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Timelog.objects.filter(id=self.timelog.id).exists())