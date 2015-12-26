#!/usr/bin/env python

from distutils.core import setup

setup(name='Tiberius',
      version='1.0',
      description='Tiberius Robot Software Suite',
      author='Cameron A. Craig',
      author_email='camieac@gmail.com',
      url='https://github.com/IonSystems/tiberius-robot/',
      packages=['tiberius', 'tiberius/control', 'tiberius/logger', 'tiberius/database', 'tiberius/utils', 'tiberius/settings'],
      platforms=['Raspberry Pi 2', 'Raspberry Pi 1'],
     )
