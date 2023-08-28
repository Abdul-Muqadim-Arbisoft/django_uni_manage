from django.test import TestCase
from .models import Project
from datetime import date

class ProjectTestCase(TestCase):
    def setUp(self):
        Project.objects.create(
            name="Sample Project",
            description="Sample Description",
            start_date=date.today(),
            end_date=date.today()  # or any other future date you prefer
        )

    def test_project_created(self):
        project = Project.objects.get(name="Sample Project")
        self.assertEqual(project.description, 'Sample Description')
