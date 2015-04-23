#!/usr/bin/env python

from setuptools import setup

setup(
    name='archieml',
    version='0.0.0',
    author='Kevin Schaul',
    author_email='kevin.schaul@gmail.com',
    url='http://kevin.schaul.io',
    description='A parser for ArchieML.',
    packages=[
        'archieml',
    ],
    entry_points = {
        'console_scripts': [
            'archieml = archieml.archieml:launch_new_instance',
        ],
    },
    test_suite = 'tests.test_archieml',
)
