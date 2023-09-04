from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from .serializers import ProjectSerializer, CommentSerializer, SupervisorLoginSerializer
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import Project, Comment, Supervisor
from user.models import CustomUser
from .views import ProjectsListView, ViewCommentsView
from datetime import date, timedelta


class SupervisorLoginViewTestCase(TestCase):
    """
    Test cases for testing the Supervisor login view.
    """

    def setUp(self):
        """Setup test data for Supervisor login tests."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword', username='test',
                                                   father_name='father', description='hell no', country="Algeria")
        self.supervisor = Supervisor.objects.create(user=self.user, expertise="Testing")

    def test_supervisor_login(self):
        """
        Test the supervisor login functionality.
        """
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'expertise': 'software E',
        }
        response = self.client.post(reverse('supervisor_login'), data)
        self.assertEqual(response.status_code, 302)  # Assuming a 200 response means successful login


class CommentViewSetTestCase(TestCase):
    """
    Test cases for the Comment view set.
    """

    def setUp(self):
        """Setup test data for Comment view set tests."""
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='test3@example.com', password='testpassword', username='test3',
                                                   father_name='father3', description='description 3',
                                                   country="Algeria")
        self.supervisor = Supervisor.objects.create(user=self.user, expertise="QA")
        self.project = Project.objects.create(name="Test Project 2", description="A second test project",
                                              start_date="2023-01-02", end_date="2023-12-31",
                                              supervisor=self.supervisor)
        self.comment = Comment.objects.create(project=self.project, user=self.user, text="Test comment")

    def test_comment_creation(self):
        """
        Test the comment creation functionality.
        """
        self.client.login(email='test3@example.com', password='testpassword')
        data = {
            'text': 'Another test comment',
            'project': self.project.id
        }
        response = self.client.post(reverse('comment-list'), data)
        self.assertEqual(response.status_code, 201)


class ProjectSerializerTestCase(TestCase):
    """
    Test cases for the Project serializer.
    """

    def setUp(self):
        """Setup test data for Project serializer tests."""
        self.user = CustomUser.objects.create(email="test@example.com", password="testpassword", username="testuser",
                                              father_name="testfather", description="testdesc", country="Algeria")
        self.supervisor = Supervisor.objects.create(user=self.user)
        self.project_data = {
            'name': 'Test Project',
            'description': 'Description for Test Project',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'students_emails': ['student@example.com'],
            'supervisor': self.supervisor.id
        }

    def test_valid_project_serializer(self):
        """Test if the Project serializer works for valid data."""
        serializer = ProjectSerializer(data=self.project_data)
        self.assertTrue(serializer.is_valid())

    def test_project_serializer_without_students(self):
        """Test if the Project serializer throws an error without students_emails."""
        data = self.project_data.copy()
        del data['students_emails']
        serializer = ProjectSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_project_serializer_representation(self):
        """Test the representation of the Project serializer."""
        project = Project.objects.create(name='Test Project', description='Description for Test Project',
                                         start_date='2023-01-01', end_date='2023-12-31', supervisor=self.supervisor)
        project.students.add(self.user)
        serializer = ProjectSerializer(project)
        expected_data = {
            'id': project.id,
            'name': 'Test Project',
            'description': 'Description for Test Project',
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'students': [self.user.id],
            'supervisor': self.supervisor.id
        }
        self.assertEqual(serializer.data, expected_data)


class CommentSerializerTestCase(TestCase):
    """
    Test cases for the Comment serializer.
    """

    def setUp(self):
        """Setup test data for Comment serializer tests."""
        self.user = CustomUser.objects.create(email="test2@example.com", password="testpassword2", username="testuser2",
                                              father_name="testfather2", description="testdesc2", country="Algeria")
        self.supervisor = Supervisor.objects.create(user=self.user)
        self.project = Project.objects.create(name='Test Project', description='Test', start_date='2023-01-01',
                                              end_date='2023-12-31', supervisor=self.supervisor)
        self.comment_data = {
            'text': 'Test Comment',
            'project': self.project.id,
            'user': self.user.id
        }

    def test_valid_comment_serializer(self):
        """Test if the Comment serializer works for valid data."""
        serializer = CommentSerializer(data=self.comment_data)
        self.assertTrue(serializer.is_valid())

    def test_comment_serializer_representation(self):
        """Test the representation of the Comment serializer."""
        comment = Comment.objects.create(text='Test Comment', project=self.project, user=self.user)
        serializer = CommentSerializer(comment)
        expected_data = {
            'id': comment.id,
            'text': 'Test Comment',
            'project': self.project.id,
            'user': self.user.id,
            'timestamp': comment.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }
        self.assertEqual(serializer.data, expected_data)


class SupervisorLoginSerializerTestCase(TestCase):
    """
    Test cases for the Supervisor login serializer.
    """

    def setUp(self):
        """Setup test data for Supervisor login serializer tests."""
        self.user = CustomUser.objects.create_user(email="supervisor@example.com", password="supervisorpassword",
                                                   username="supervisoruser", father_name="supervisorfather",
                                                   description="supervisordesc", country="Algeria")
        self.supervisor = Supervisor.objects.create(user=self.user)

    def test_valid_login(self):
        """Test if the Supervisor login serializer works for valid credentials."""
        data = {
            'email': 'supervisor@example.com',
            'password': 'supervisorpassword'
        }
        serializer = SupervisorLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_login(self):
        data = {
            'email': 'supervisor@example.com',
            'password': 'wrongpassword'
        }
        serializer = SupervisorLoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_non_supervisor_login(self):
        user = CustomUser.objects.create_user(email="notasupervisor@example.com", password="testpassword3",
                                              username="nonsupervisoruser", father_name="nonsupervisorfather",
                                              description="nonsupervisordesc", country='Algeria')
        data = {
            'email': 'notasupervisor@example.com',
            'password': 'testpassword3'
        }
        serializer = SupervisorLoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class ProjectsListViewTestCase(TestCase):
    """
    Test cases for the ProjectsListView.
    """

    def setUp(self):
        """Setup test data for ProjectsListView tests."""
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword', username='test',
                                                   father_name='father', description='description', country='Algeria')
        self.supervisor = Supervisor.objects.create(user=self.user, expertise="Testing")
        self.project1 = Project.objects.create(name="Test Project 1", supervisor=self.supervisor,
                                               start_date=date.today(), end_date=date.today() + timedelta(days=10))

        self.project2 = Project.objects.create(name="Test Project 2", supervisor=self.supervisor,
                                               start_date=date.today(), end_date=date.today() + timedelta(days=10))
        self.factory = RequestFactory()

    def test_project_list_view(self):
        """Test that ProjectsListView displays the correct list of projects."""
        request = self.factory.get(reverse('projects_list'))
        request.user = self.user
        response = ProjectsListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project 1')
        self.assertContains(response, 'Test Project 2')


class ViewCommentsViewTestCase(TestCase):
    """
    Test cases for the ViewCommentsView.
    """

    def setUp(self):
        """Setup test data for ViewCommentsView tests."""
        self.user = CustomUser.objects.create_user(email='commenter@example.com', password='testpassword',
                                                   username='commenter',
                                                   father_name='father_commenter', description='description_commenter',
                                                   country='Algeria'
                                                   )
        self.supervisor = Supervisor.objects.create(user=self.user, expertise="QA")
        self.project = Project.objects.create(name="Test Project", supervisor=self.supervisor, start_date=date.today(),
                                              end_date=date.today() + timedelta(days=10))

        self.comment = Comment.objects.create(project=self.project, user=self.user, text="Initial Comment")
        self.factory = RequestFactory()

    def test_view_comments_get(self):
        """Test the GET method of ViewCommentsView."""
        request = self.factory.get(
            reverse('view_comments', kwargs={'project_id': self.project.id}))
        request.user = self.user
        response = ViewCommentsView.as_view()(request, project_id=self.project.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Comment')

    def test_view_comments_post(self):
        """Test the POST method of ViewCommentsView."""
        request = self.factory.post(
            reverse('view_comments', kwargs={'project_id': self.project.id}),
            {'text': 'New Comment'})
        request.user = self.user
        # Mock Django's messages framework for the request
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        response = ViewCommentsView.as_view()(request, project_id=self.project.id)
        self.assertEqual(response.status_code, 302)  # Check if redirect
        new_comment = Comment.objects.filter(text="New Comment").first()
        self.assertIsNotNone(new_comment)

# [Include your other tests here, which you've provided previously]
