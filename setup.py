import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-translation-checker',
    version='0.1',
    packages=['translation_checker'],
    include_package_data=True,
    license='MIT License',
    description='Django app for identifying missing translations.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/City-of-Helsinki/django-translation-checker',
    author='City of Helsinki',
    author_email='dev@hel.fi',
    install_requires=[
        'Django',
        'django-parler',
        'polib',
    ],
    classifiers=[
        'Environment :: Console',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Localization',
        'Topic :: Utilities',
    ],
)
