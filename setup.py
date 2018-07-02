#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'asyncpg',
    'sanic',
    'sanic_cors'
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(manqx): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pg_api',
    version='0.1.0',
    description="api backend pg",
    long_description=readme + '\n\n' + history,
    author="Man Quanxing",
    author_email='manquanxing@mingvale.com',
    url='https://github.com/manqx/pg_api',
    packages=find_packages(include=['pg_api']),
    entry_points={
        'console_scripts': [
            'pg-api=pg_api.cli:main',
            'manage=pg_api.manage:main',
            'create-table=pg_api.create_tables:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pg_api',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
