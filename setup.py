# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='popy',
    description='Parser for GNU Po files',
    long_description=open('README.rst').read(),
    version='0.1.3',
    packages=['popy'],
    author='Murat Aydos',
    author_email='murataydos@yandex.com',
    url='https://github.com/murataydos/popy',
    license='GPL',
    zip_safe=False,
    include_package_data=True
)
