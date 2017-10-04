import os

import polib
from django.test import TestCase
from django.conf import settings

from dsmr_backend.tests.mixins import InterceptStdoutMixin


class TestTranslations(InterceptStdoutMixin, TestCase):
    """ NOTE: This also regenerates translations! """
    def setUp(self):
        # A bit of a hack to detect all languages set, excluding the default one (should be base).
        self.locales = [pair[0] for pair in settings.LANGUAGES]
        self.locales.remove(settings.LANGUAGE_CODE)

    def test_available_locales(self):
        """ Check for Dutch only, as a reminder to test, should we support multiple languages. """
        self.assertEqual(self.locales, ['nl'])

    def test_percent_translated(self):
        """ Test whether localization files are 100% translated. """
        self._intercept_command_stdout(
            'makemessages',
            locale=self.locales,
            no_location=True,
            no_wrap=True,
            # Weird bug/collision with coverage reports, crashing the test.
            ignore_patterns=['coverage_report/*'],
        )
        self._intercept_command_stdout('compilemessages')

        for current_locale in self.locales:
            po_file_path = os.path.join(
                settings.LOCALE_PATHS[0], current_locale, 'LC_MESSAGES', 'django.po'
            )
            po = polib.pofile(po_file_path)
            self.assertEqual(po.percent_translated(), 100)
