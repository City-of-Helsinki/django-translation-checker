# Django App for Identifying Missing Translations

This app is a helper utility that can be used to check for missing `gettext` or `parler` missing in a Django project.


## Prerequisites
This utility requires GNU gettext tools 0.15 or later. You can install it with e.g.:
```sh
apt install gettext
```

## Installation

Install the app with `pip`:
```sh
pip install git+https://github.com/City-of-Helsinki/django-translation-checker.git@master
```

Add the app to Django settings:
```py
...
INSTALLED_APPS = (
...
    'translation_checker',
)
...
```

## Configuration

The app requires that the following Django settings are present:
```py
# Default language for the Django application
LANGUAGE_CODE = 'fi'

# Languages supported by the application
LANGUAGES = (
    ('fi', 'Finnish'),
    ('sv', 'Swedish'),
    ('en', 'English'),
)

# Path for the gettext '.po' translation files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
```

## Usage and Notes

To run the checker, use:
```sh
./manage.py check_translations
```

The checker supports the following arguments:
```
optional arguments:
  --no-color            Don't colorize the command output.
  --exclude LANG        Exclude language from check

gettext options:
  --gettext-check-all   Check all translatable strings
  --gettext-source-has-language LANG
                        Use source code strings for language LANG
  --no-gettext          Do not check gettext translations
  --no-gettext-update   Do not update gettext translation files

parler options:
  --no-parler           Do not check parler translations
```

By default the checker only notifies about those gettext strings that have at least one translation. To get notifications from all translatable gettext strings use `--gettext-check-all`.

The strings embedded in source code are not considered as translated unless the option `--gettext-source-has-language` is used.

The utility runs Django `makemessages` for all languages listed in `LANGUAGES` setting unless `--no-gettext-update` option is used.
