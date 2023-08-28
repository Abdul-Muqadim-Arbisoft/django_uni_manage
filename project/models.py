from django.db import models
from user.models import CustomUser


class Supervisor(models.Model):
    """
    Represents a supervisor who oversees projects.
    Has a one-to-one relation with a custom user and possesses expertise in a specific domain.
    """
    user = models.OneToOneField(CustomUser,
                                on_delete=models.CASCADE,
                                help_text="The associated user for this supervisor."
                                )
    expertise = models.CharField(max_length=200, help_text="Area of expertise of the supervisor.")


class Project(models.Model):
    """
    Represents a project supervised by a supervisor and possibly worked on by multiple students.
    """
    name = models.CharField(max_length=200, help_text="Name of the project.")
    description = models.TextField(help_text="Description or details of the project.")
    start_date = models.DateField(help_text="The start date of the project.")
    end_date = models.DateField(help_text="The expected end date of the project.")
    students = models.ManyToManyField(CustomUser,
                                      related_name='student_projects',
                                      help_text="Students associated with this project."
                                      )
    supervisor = models.ForeignKey(Supervisor,
                                   on_delete=models.CASCADE,
                                   related_name='supervised_projects',
                                   help_text="The supervisor overseeing this project."
                                   )


class Comment(models.Model):
    """
    Represents a comment made by a user on a project.
    Stores the associated project, the user who commented, the text of the comment, and the timestamp of when
    it was made.
    """
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                help_text="The project this comment is associated with."
                                )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="The user who made this comment.")
    text = models.TextField(help_text="Text of the comment.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The time when the comment was created.")
