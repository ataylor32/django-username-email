from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='django-username-email',

    version='2.5.3',

    description='Custom Django User model that makes email the USERNAME_FIELD.',
    long_description=long_description,

    url='https://github.com/tmm/django-username-email/',

    author='Adam Taylor',
    author_email='ataylor32@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Operating System :: OS Independent',
    ],
    keywords='user email username',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'django>=3.2',
    ]
)
