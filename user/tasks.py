# tasks.py

from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, ReminderSetting


@shared_task(bind=True)
def send_welcome_email(self, email, username):
    try:
        subject = "Welcome to Our Uni Management Site!"
        message = f"""
        <html>
            <head></head>
            <body>
                <p>Hello {username},</p>
                <p>Thank you for registering with us. We're excited to have you on board!</p>
                <p>Best Regards,</p>
                <p>Your Team</p>
            </body>
        </html>
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=message)
    except Exception as e:
        # Here you can log the error or even retry the task if necessary.
        self.retry(countdown=60 * 5, exc=e, max_retries=3)


@shared_task(bind=True)
def check_last_login_and_send_email(self):
    # Get the duration and duration_type from the ReminderSetting
    try:
        reminder_setting = ReminderSetting.objects.first()
        duration = reminder_setting.duration
        duration_type = reminder_setting.duration_type
    except AttributeError:
        # Default values in case the setting isn't found
        duration = 1
        duration_type = 'minutes'  # Setting default to days for this test

    if duration_type == 'seconds':
        time_threshold = datetime.now() - timedelta(seconds=duration)
    elif duration_type == 'hours':
        time_threshold = datetime.now() - timedelta(hours=duration)
    elif duration_type == 'days':
        time_threshold = datetime.now() - timedelta(days=duration)
    else:  # default to minutes
        time_threshold = datetime.now() - timedelta(minutes=duration)

    # Get all users who joined more than the time_threshold ago
    users_to_notify = CustomUser.objects.filter(last_login__lt=time_threshold)

    for user in users_to_notify:
        subject = "We appreciate you!"
        message = f"Hello {user.username},\n\n We have noticed that its been a while since you last visited. We would love to see you back on our platform!"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
