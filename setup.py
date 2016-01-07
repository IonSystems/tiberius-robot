#!/usr/bin/env python

from distutils.core import setup

setup(name='Tiberius',
      version='1.0',
      description='Tiberius Robot Software Suite',
      author='Cameron A. Craig',
      author_email='camieac@gmail.com',
      url='https://github.com/IonSystems/tiberius-robot/',
      packages=['tiberius', 'tiberius/control', 'tiberius/logger', 'tiberius/database', 'tiberius/utils', 'tiberius/config', 'tiberius/smbus_dummy'],
      data_files    =   [
                            ('/etc/tiberius', ['tiberius/config/tiberius_conf.conf']),
                            ('/etc/tiberius', ['tiberius/smbus_dummy/smbus_database.db']),
                            #('/etc/tiberius', ['tiberius/database/polyhedra_databse.db'])
                        ],
      platforms=['Raspberry Pi 2', 'Raspberry Pi 1'],
     )
