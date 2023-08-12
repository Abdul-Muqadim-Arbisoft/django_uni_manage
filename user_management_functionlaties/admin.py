from django.contrib import admin
from .models import CustomUser, DateTimeRecord,Job

admin.site.register(CustomUser)
admin.site.register(DateTimeRecord)
admin.site.register(Job)
# Register your models here.
