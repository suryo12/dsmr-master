from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import APISettings


@admin.register(APISettings)
class APISettingsAdmin(SingletonModelAdmin):
    list_display = ('allow', 'auth_key')
