import os
import sys

from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.translation import activate as activate_translation
from parler.models import TranslatableModel
from polib import pofile


class Command(BaseCommand):
    help = 'Check project for missing translations'

    def add_arguments(self, parser):
        parser.add_argument('--exclude',
                            action='append',
                            metavar='LANG',
                            default=[],
                            help='Exclude language from check')

        gettext_group = parser.add_argument_group('gettext options')
        gettext_group.add_argument('--gettext-check-all',
                                   action='store_true',
                                   help='Check all translatable strings')
        gettext_group.add_argument('--gettext-source-has-language',
                                   action='store',
                                   metavar='LANG',
                                   help='Use source code strings for language LANG')
        gettext_group.add_argument('--no-gettext',
                                   action='store_false',
                                   help='Do not check gettext translations')
        gettext_group.add_argument('--no-gettext-update',
                                   action='store_false',
                                   help='Do not update gettext translation files')

        parler_group = parser.add_argument_group('parler options')
        parler_group.add_argument('--no-parler',
                                  action='store_false',
                                  help='Do not check parler translations')

    def handle(self, *args, **options):
        langs = [lang[0] for lang in settings.LANGUAGES if lang[0] not in options['exclude']]
        activate_translation(settings.LANGUAGE_CODE)

        self.stdout.write('')
        self._show_configured_languages(langs)
        self.stdout.write('')
        missing_translations = False
        if options['no_gettext']:
            if options['no_gettext_update']:
                self._update_gettext_translation_files(langs)
                self.stdout.write('')
            missing_translations |= self._check_gettext_translations(langs,
                                                                     options['gettext_check_all'],
                                                                     options['gettext_source_has_language'])
            self.stdout.write('')
        if options['no_parler']:
            missing_translations |= self._check_parler_translations(langs)
            self.stdout.write('')

        if missing_translations:
            sys.exit(1)

    def _show_configured_languages(self, languages):
        self.stdout.write('Configured languages:')
        for lang in settings.LANGUAGES:
            if lang[0] in languages:
                self.stdout.write('  {} - {}'.format(
                    self.style.SUCCESS(lang[0]),
                    lang[1]))
            else:
                self.stdout.write('  {} - {} {}'.format(
                    self.style.NOTICE(lang[0]),
                    lang[1],
                    self.style.WARNING('(excluded)')))

    def _update_gettext_translation_files(self, languages):
        self.stdout.write('Update gettext translations:')
        call_command('makemessages', locale=languages)

    def _check_gettext_translations(self, languages, check_all=False, source_language=None):
        def _load_po(language):
            filepath = os.path.join(settings.LOCALE_PATHS[0],
                                    language,
                                    'LC_MESSAGES',
                                    'django.po')
            if os.path.isfile(filepath):
                return pofile(filepath)
            self.stdout.write('{} {}'.format(
                self.style.WARNING('Could not find language file for'),
                self.style.ERROR(language)))

        langfiles = {lang: _load_po(lang) for lang in languages}
        translations = {}
        for lang, po in langfiles.items():
            if check_all or lang == source_language:
                for entry in po.untranslated_entries() if po else []:
                    if lang == source_language:
                        translations.setdefault(entry.msgid, []).append(lang)
                    else:
                        translations.setdefault(entry.msgid, [])
            for entry in po.translated_entries() if po else []:
                translations.setdefault(entry.msgid, []).append(lang)

        missing = {translation: set(languages) - set(langs)
                   for translation, langs in translations.items()
                   if set(languages) - set(langs)}
        if missing:
            self.stdout.write('Missing gettext translations:')
            self.stdout.writelines(['  {} - {}'.format(
                self.style.ERROR(' '.join([lang if lang in missing[key] else '  ' for lang in languages])), key)
                for key in sorted(missing.keys())])
            return True

        return False

    def _check_parler_translations(self, languages):
        missing = {}
        for model in apps.get_models():
            if isinstance(model(), TranslatableModel):
                translations = {}
                for item in model.objects.all():
                    for lang in item.get_available_languages():
                        translated_item = item.get_translation(lang)
                        for field in translated_item.get_translated_fields():
                            if getattr(translated_item, field):
                                translation = '<{}: {}>.{}'.format(
                                    self.style.WARNING(model().__class__.__name__),
                                    item, self.style.WARNING(field)
                                )
                                translations.setdefault(translation, []).append(lang)

                missing.update({translation: set(languages) - set(langs)
                                for translation, langs in translations.items()
                                if set(languages) - set(langs)})
        if missing:
            self.stdout.write('Missing parler translations:')
            self.stdout.writelines(['  {} - {}'.format(
                self.style.ERROR(' '.join([lang if lang in missing[key] else '  ' for lang in languages])), key)
                for key in sorted(missing.keys())])
            return True

        return False
