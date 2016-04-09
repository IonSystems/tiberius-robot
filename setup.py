#!/usr/bin/env python
from setuptools import setup
from setuptools.command.install import install
from subprocess import check_output, CalledProcessError
import os
import sys
from optparse import OptionParser

'''*****************************************
        Utility Functions
*****************************************'''


def is_windows():
    return 'nt' in os.name


def is_pi():
    return 'arm' in os.uname()[4]


def is_linux():
    return "linux" in sys.platform


def is_apt_get():
    result = check_output("type apt-get")
    if "not found" in result:
        return False
    else:
        return True


def is_text_found(text, file):
    try:
        if(text in check_output(
         "grep -r " + text + " " + file, shell=True)):
            return True
        else:
            return False
    except CalledProcessError:
        return False


def is_folder_found(dir):
    found_result = "found!"
    try:
        if(found_result in check_output(
         "[ -d " + dir + " ] && echo " + "'" + found_result + "'",
         shell=True)):
            print "dir: " + dir + " found."
            return True
        else:
            print "dir: " + dir + " not found."
            return False
    except CalledProcessError:
        print "dir: " + dir + " not found."
        return False


def is_file_found(file):
    found_result = "found!"
    try:
        if(found_result in check_output(
         "[ -f " + file + " ] && echo 'found!'", shell=True)):
            return True
        else:
            return False
    except CalledProcessError:
        return False


class PostInstallDependencies(install):
    '''
        Install all dependencies that cannot be easily satisfied by setuptools.
        TODO: Encorporate more of this install process into setuptools.
    '''
    def run(self):
        if is_windows():
	    print "Installing on Windows."
        elif is_pi():
	    print "Installing on Raspberry Pi."
            self.install_deps_pi()
            self.install_poly_pi()
        elif is_linux():
	    print "Installing on Linux."
            self.install_deps_linux()
            self.install_poly_linux()
            self.create_lidar_executable()
        else:
            print 'No suitable operating system detected, terminating install'
            sys.exit()

        install.do_egg_install(self)

    def install_deps_pi(self):
        self.install_if_missing("build-essential")
        self.install_if_missing("python-dev")
        self.install_if_missing("libffi-dev")
        self.install_if_missing("libi2c-dev")
        self.install_if_missing("i2c-tools")
	self.un_blacklist_i2c()
	self.enable_modules_i2c()

    def create_lidar_executable(self):
        check_output("cd ~/git/tiberius-robot/tiberius/autonomy/readlidar", shell=True)
        check_output("g++ -pthread -lrt rplidar_driver.cpp thread.cpp net_serial.cpp timer.cpp readlidar.cpp -o readlidar", shell=True)
        print "creating lidar executable"

    def install_deps_linux(self):
        print "Checking for missing packages"
        self.install_if_missing("build-essential")
        self.install_if_missing("python-dev")
        self.install_if_missing("libffi-dev")

    def un_blacklist_i2c(self):
        print "Removing I2C from blacklist on Raspberry Pi"
        blacklist_dir = "/etc/modprobe.d/raspi-blacklist.conf"
        enable_command = "sed -i 's/blacklist i2c-bcm2708/#blacklist" \
         " i2c-bcm2708/g' " + blacklist_dir
        check_output(enable_command, shell=True)

    def enable_modules_i2c(self):
        print "Adding i2c-dev and i2c-bcm2708 to enabled modules"
        modules_dir = "/etc/modules"
        if(is_text_found("i2c-dev", modules_dir)):
            print "i2c-dev already enabled"
        else:
            print "Enabling i2c-dev"
            enable_command = "echo 'i2c-dev' | sudo tee -a " + modules_dir
            check_output(enable_command, shell=True)

        if(is_text_found("i2c-bcm2708", modules_dir)):
            print "i2c-bcm2708 already enabled"
        else:
            enable_command = "echo 'i2c-bcm2708' | sudo tee -a " + \
            modules_dir
            check_output(enable_command, shell=True)

    def is_package_installed(self, package_name):
        try:
            result = check_output(
                "dpkg-query -W -f='${Status} ${Version}\n' " +
                package_name,
                shell=True)
        except CalledProcessError:
            try:
                result = check_output("dpkg -s " + package_name, shell=True)
            except CalledProcessError:
                result = "not-installed"
        if("not-installed" in result):
            return False
        else:
            return True

    def install_package(self, package_name):
        try:
            self.install_aptget(package_name)
        except CalledProcessError:
            # Apt-get might not be available, so we should try dnf instead
            try:
                res = check_output(
                    "sudo dnf -y install " +
                    package_name,
                    shell=True)
            except CalledProcessError:
                print package_name + " failed to install."

    def install_aptget(self, package_name):
        res = check_output(
            "sudo apt-get -y install " +
            package_name,
            shell=True)

    def install_yum(package_name):
        res = check_output(
            "sudo yum -y install " +
            package_name,
            shell=True)

    def install_if_missing(self, package_name):
        if not (self.is_package_installed(package_name)):
            print "Installing " + package_name
            self.install_package(package_name)
        else:
            print package_name + " already installed"

    def remove_file(self, filename):
        check_output("sudo rm " + filename, shell=True)

    def is_pi(self):
        return os.uname()[4][:3] == 'arm'

    def install_poly_windows(self):
        print "Polyhedra on windows is currently not supported."
        # TODO: Install script for polyhedra on windows
        # self.install_odbc("windows")
        # self.install_pyodbc("windows")
        # self.install_poly_driver("", "")
        # self.install_poly("", "")

    def install_poly_pi(self):
        self.install_odbc("pi")
        self.install_pyodbc("pi")
        self.install_poly_driver("vendor/polyhedra-driver/raspi/linux/raspi/bin/libpolyod32.so", "/home/pi/libpolyod32.so")
        self.install_poly("vendor/polyhedra-lite/raspi/", "/home/pi/poly9.0/", "pi")
        # self.install_poly_startup_task()

    def install_poly_linux(self):
        self.install_odbc("linux")
        self.install_pyodbc("linux")
        self.install_poly_driver("vendor/polyhedra-driver/linux/linux/i386/bin/libpolyod32.so", "~/libpolyod32.so")
        self.install_poly("vendor/polyhedra-lite/linux/", "~/poly9.0/", "linux")

    def install_poly_driver(self, src_dir, dst_dir):
        # Linux
        # Move the polyhedra driver to the user's directory
        if not is_file_found(dst_dir):
            result = check_output("cp " + src_dir + " " + dst_dir, shell=True)
        return

    def install_poly(self, src_dir, dst_dir, platform):
        # Linux
        # Copy the polyhedra executables to the user's directory.
        if not is_folder_found(dst_dir):
            check_output("sudo cp -r " + src_dir + " " + dst_dir, shell=True)
        else:
            print "Polyhedra lite executables already in place, nothing to be done here."

        # Ensure the polyhedra executables are on the command path
        bashrc_dir = "/etc/bash.bashrc"
        if "linux" in platform:
            bash_command = "export PATH=~/poly9.0/linux/linux/i386/bin/:$PATH"
        elif "pi" in platform:
            bash_command = "export PATH=/home/pi/poly9.0/linux/raspi/bin/:$PATH"
        elif "windows" in platform:
            print "Cannot currently install Polyhedra on windows."
            bash_command = None
        already_done = is_text_found("poly9.0/linux/raspi/bin", bashrc_dir)
        command_available = bash_command is not None
        if not already_done and command_available:
            command = "echo '" + bash_command + "' | sudo tee -a " + bashrc_dir
            check_output(command, shell=True)

    def install_poly_startup_task(self):
        from crontab import CronTab
        print "poly_start configuration starting..."

        command = "/home/pi/poly9.0/linux/raspi/bin/rtrdb -r data_service=8001 db"
        comment = "poly_start"
        cron = CronTab(user='root')
        if not cron.find_comment('poly_start'):
            print "Installing poly_start crontab..."
            job = cron.new(command=command, comment=comment)
            job.every_reboot()
            cron.write()
            if job.is_valid():
                print "poly_start crontab successfully installed."
            else:
                print "poly_start crontab failed to install"
        else:
            print "poly_start crontab already installed"
            print "removing old job"
            oldjob = cron.find_comment('poly_start')
            print ('OldJob', oldjob)
            #cron.remove(oldjob)
            print "Installing poly_start crontab..."
            job = cron.new(command=command, comment=comment)
            job.every_reboot()
            cron.write()
            if job.is_valid():
                print "poly_start crontab successfully installed."
            else:
                print "poly_start crontab failed to install"
        print "Listing all crontab jobs:"
        for cronjob in cron:
            print cronjob

        print "poly_start configuration finished"



    def install_pyodbc(self, platform):
        if "pi" in platform or "linux" in platform:
            self.install_if_missing("python-pyodbc")
        elif "windows" in platform:
            # TODO: pyodbc on windows
            print "ODBC on windows currently not supported, skipping."

    def install_odbc(self, platform):
        if "pi" in platform or "linux" in platform:
            self.install_if_missing("unixodbc")
            self.install_if_missing("unixodbc-dev")

            # Remove default odbc config files,
            # so that setuptools replaces them
            self.remove_file('/etc/odbc.ini')
            self.remove_file('/etc/odbcinst.ini')
        elif "windows" in platform:
            # TODO: pyodbc on windows
            print "ODBC on windows currently not supported, skipping."

if is_windows():
    # Parameters for windows operating systems
    data_directory = 'D:\\tiberius'
    odbc_directory = data_directory
    requirements = ['enum34',
                    'autopep8',
                    'pynmea',
                    'pyserial',
                    'falcon',
                    'gunicorn',
                    'requests']

else:
    # Parameters for Linux-based operating systems
    data_directory = '/etc/tiberius'
    odbc_directory = '/etc'
    requirements = ['enum34',
                    'autopep8',
                    'pynmea',
                    'pyserial',
                    'smbus-cffi',
                    'falcon',
                    'gunicorn',
                    'python-crontab',
                    'requests']

setup(name='Tiberius',
      version='1.0',
      description='Tiberius Robot Software Suite',
      author='Cameron A. Craig',
      author_email='camieac@gmail.com',
      url='https://github.com/IonSystems/tiberius-robot/',
      packages=[
          'tiberius',
          'tiberius/control',
          'tiberius/control/drivers',
          'tiberius/control/robotic_arm',
          'tiberius/control_api',
          'tiberius/control_api/tasks',
          'tiberius/diagnostics',
          'tiberius/navigation/gps',
          'tiberius/navigation',
          'tiberius/logger',
          'tiberius/database',
          'tiberius/database_wrapper',
          'tiberius/utils',
          'tiberius/config',
          'tiberius/smbus_dummy'],
      data_files=[
          (data_directory, ['tiberius/config/tiberius_conf.conf']),
          (data_directory, ['tiberius/smbus_dummy/smbus_database.db']),
          (odbc_directory, ['vendor/polyhedra-driver/odbc.ini']),
          (odbc_directory, ['vendor/polyhedra-driver/odbcinst.ini']),
      ],
      platforms=['Raspberry Pi 2', 'Raspberry Pi 1'],
      install_requires=requirements
      #cmdclass={
      # 'install': PostInstallDependencies},
      )
