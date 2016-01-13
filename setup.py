#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install
from subprocess import check_output, CalledProcessError

class PostInstallDependencies(install):
	def run(self):
		print "Checking for missing packages"
		self.install_if_missing("build-essential")
		self.install_if_missing("libi2c-dev")
		self.install_if_missing("i2c-tools")
		self.install_if_missing("python-dev")
		self.install_if_missing("libffi-dev")
		
		print "Removing I2C from blacklist on Raspberry Pi"
		blacklist_dir = "/etc/modprobe.d/raspi-blacklist.conf"
		enable_command = "sed -i 's/blacklist i2c-bcm2708/#blacklist i2c-bcm2708/g' " + blacklist_dir
		check_output(enable_command, shell = True)

		print "Adding i2c-dev and i2c-bcm2708 to enabled modules"
		modules_dir = "/etc/modules"
		if(self.is_text_found("i2c-dev", modules_dir)):
			print "i2c-dev already enabled"
		else:
			print "Enabling i2c-dev"
			enable_command = "echo 'i2c-dev' | sudo tee -a " + modules_dir
			check_output(enable_command, shell = True)

		if(self.is_text_found("i2c-bcm2708", modules_dir)):
			print "i2c-bcm2708 already enabled"
		else:
			print "Enabling i2c-bcm2708"
			enable_command = "echo 'i2c-bcm2708' | sudo tee -a " + modules_dir
			check_output(enable_command, shell = True)

		#Continue with the rest of the installation process.
		install.do_egg_install(self)

	def is_text_found(self, text, file):
		try:
			if(text in check_output("grep -r " + text + " " + file, shell = True)):
				return True
			else:
				return False
		except CalledProcessError:
			return False 

	def is_package_installed(self, package_name):
		try:
			result = check_output("dpkg-query -W -f='${Status} ${Version}\n' " + package_name, shell = True)
			if("not-installed" in result):
				return False
			else:
				return True
		except CalledProcessError:
			return False

	def install_package(self, package_name):
		try:
			res = check_output("sudo apt-get -y install " + package_name, shell = True)
		except CalledProcessError:
			print package_name + " failed to install."

	def install_if_missing(self, package_name):
		if not (self.is_package_installed(package_name)):
			print "Installing " + package_name
			self.install_package(package_name)
		else:
			print package_name + " already installed"

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
      install_requires=['enum34', 'smbus-cffi', 'pyttsx'],
      cmdclass={'install':PostInstallDependencies},
     )
