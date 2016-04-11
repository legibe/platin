# -*- coding: utf-8 -*-

import os
import sys

import setuptools


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

setuptools.setup(
    name='platin',
    version='0.0.7',
    description='Set of utility libs',
    long_description=readme + '\n\n' + history,
    author='Platform Intelligence',
    author_email='platin@datasift.com',
    url='https://github.com/datasift/platin',
    packages=[
        'platin',
        'platin.core',
        'platin.datasift',
        'platin.datasift.csdl',
        'platin.datasift.jira',
        'platin.datasift.salesforce',
        'platin.datasift.zuora',
        'platin.datasift.databases',
        'platin.datasift.databases.definitionmanager',
        'platin.datasift.databases.journal',
        'platin.datasift.databases.mask',
        'platin.datasift.databases.ratecard',
        'platin.gmail',
        'platin.httpservices',
        'platin.httpservices.lib',
        'platin.language',
        'platin.mysql',
        'platin.scheduler',
        'platin.scheduler.include',
        'platin.scheduler.bin',
    ],
    package_dir={'platin': 'platin'},
    package_data={
        'platin.core': ['*.json'],
        'platin.datasift.dszuora.catalogue.schema': ['*.json'],
        'platin.scheduler.include': ['*.h'],
        'platin.scheduler.bin': ['*'],
    },
    include_package_data=True,
    install_requires=[
        'MySQL-python >= 1.2.5',
        'Twisted >= 14.0.0',
        'zope.interface >= 3.6.0',
    ],
    license="Internal",
    zip_safe=False,
    keywords='platin',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Internal',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
