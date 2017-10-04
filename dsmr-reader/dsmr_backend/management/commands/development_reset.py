from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

from dsmr_backup.models.settings import BackupSettings, DropboxSettings
from dsmr_mindergas.models.settings import MinderGasSettings
from dsmr_notification.models.settings import NotificationSetting
from dsmr_api.models import APISettings


class Command(BaseCommand):
    help = _('Resets the environment for development purposes. Not intended for production.')

    def handle(self, **options):
        if not settings.DEBUG:
            raise CommandError(_('Intended usage is NOT production! Only allowed when DEBUG = True'))

        # Just wipe all settings which can affect the environment.
        APISettings.objects.update(allow=True, auth_key='test')
        BackupSettings.objects.update(daily_backup=False)
        DropboxSettings.objects.update(access_token=None)
        MinderGasSettings.objects.update(export=False, auth_token=None)
        NotificationSetting.objects.update(send_notification=False, api_key=None)

        try:
            # Reset passwd.
            admin = User.objects.get(pk=1)
        except User.DoesNotExist:
            pass
        else:
            admin.set_password('admin')
            admin.save()
