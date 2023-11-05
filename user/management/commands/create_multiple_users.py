from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random
from user.models import CustomUser


class Command(BaseCommand):
    """
    Django management command to create random CustomUser objects with the specified
    number of users. Each user is created with random values for username, email,
    father_name, description, and software_engineering_experience fields.

    This command is useful for generating random user data for testing or development purposes.
    """

    help = 'Create random users'

    def add_arguments(self, parser):
        """
        Add a custom argument to the command.

        total: The number of users to be created.
        """
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        """
        The handle method is called when the command is run. It creates the specified number
        of random CustomUser objects and saves them to the database using bulk_create.
        """
        total = kwargs['total']
        user_list = []

        for i in range(total):
            user = CustomUser(
                username=get_random_string(length=10),
                email=f'user{i}@example.com',
                father_name=get_random_string(length=10),
                description=get_random_string(length=100),
                software_engineering_experience=random.randint(0, 20),
            )
            user_list.append(user)

        CustomUser.objects.bulk_create(user_list)
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} random users'))
