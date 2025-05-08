from django.contrib import admin
from apps.custom_auth.models import CustomUser

# Register your models here.
admin.site.register(CustomUser)