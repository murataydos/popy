# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='popy',
    description='Parser for GNU Po files',
    long_description=open('README.rst').read(),
    version='0.3.0',
    packages=['popy'],
    author='Murat Aydos',
    author_email='murataydos@yandex.com',
    url='https://github.com/murataydos/popy',
    license='MIT',
    zip_safe=False,
    include_package_data=True
)
