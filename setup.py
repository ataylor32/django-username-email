from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='django-username-email',

    version='2.4.1',

    description='Custom Django User model that makes email the USERNAME_FIELD.',
    long_description=long_description,

    url='https://github.com/tmm/django-username-email/',

    author='Tom Meagher',
    author_email='tom@meagher.co',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Operating System :: OS Independent',
    ],
    keywords='user email username',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'django',
    ]
)
