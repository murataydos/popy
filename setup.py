# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='popy',
    description='Parser for GNU Po files',
    long_description=open('README.rst').read(),
    version='0.1.0',
    packages=find_packages(),
    author='Murat Aydos',
    author_email='murataydos@yandex.com',
    url='https://github.com/murataydos/popy',
    license='GNU GENERAL PUBLIC LICENSE, see LICENCE',
    zip_safe=False,
    include_package_data=True
)
