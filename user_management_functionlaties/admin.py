from django.contrib import admin
from .models import CustomUser, DateTimeRecord

admin.site.register(CustomUser)
admin.site.register(DateTimeRecord)
# Register your models here.
