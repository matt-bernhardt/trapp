# -*- coding: utf-8 -*-
"""
Trapp, a python package for linking, analyzing, and extending soccer data.
"""

import io
from setuptools import find_packages, setup


with io.open('LICENSE') as f:
    license = f.read()


setup(
    name='trapp',
    version='0.3.0-alpha1',
    description='Link, analyze, and extend soccer data',
    url='https://github.com/matt-bernhardt/trapp',
    license=license,
    author='Matt Bernhardt',
    author_email='matt.j.bernhardt@gmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'xlrd',
        'mysql-connector-python',
    ],
    dependency_links=[
        'http://dev.mysql.com/downloads/connector/python/',
    ],
    entry_points={
        'console_scripts': ['trapp=trapp.command_line:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intendend Audience :: Other Audience',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
