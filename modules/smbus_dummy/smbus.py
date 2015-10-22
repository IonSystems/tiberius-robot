# smbus.py - cffi based python bindings for SMBus based on smbusmodule.c
# Copyright (C) 2013-2015 <david.schneider@bivab.de>
#
# smbusmodule.c - Python bindings for Linux SMBus access through i2c-dev
# Copyright (C) 2005-2007 Mark M. Hoffman <mhoffman@lightlink.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

'''
    This module simulates an I2C network for platforms with no I2C capability.
    The module is based on https://github.com/bivab/smbus-cffi.
'''

import os
import sys
sys.path.insert(0, '../logger')
#import logger.logger as logger
from logger import logger as logger
import logging

from util import validate

class SMBus(object):
    """SMBus([bus]) -> SMBus
    Return a new SMBus object that is (optionally) connected to the
    specified I2C device interface.
    """

    def __init__(self, bus=-1):
        self.logger = logging.getLogger('tiberius.smbus_dummy.SMBus')
        self.logger.info('Dummy smbus interface created')

    def close(self):
        """close()

        Disconnects the object from the bus.
        """
        self.logger.info('Dummy smbus disconnected')

    def dealloc(self):
        self.logger.info('Dummy smbus deallocated')

    def open(self, bus):
        """open(bus)

        Connects the object to the specified SMBus.
        """
        bus = int(bus)
        path = "/dev/i2c-%d" % (bus,)
        if len(path) >= MAXPATH:
                raise OverflowError("Bus number is invalid.")
        try:
            self.logger.info('Dummy smbus opened with path %s', path)
        except OSError as e:
            raise IOError(e.errno)

    def _set_addr(self, addr):
        """private helper method"""
        if self._addr != addr:
            self.logger.info('Dummy smbus address set to %s', addr)
            self._addr = addr

    @validate(addr=int)
    def write_quick(self, addr):
        """write_quick(addr)

        Perform SMBus Quick transaction.
        """
        self._set_addr(addr)
        self.logger.info('Dummy smbus quick write with addr %s', addr)

    @validate(addr=int)
    def read_byte(self, addr):
        """read_byte(addr) -> result

        Perform SMBus Read Byte transaction.
        """
        self.logger.info('Write block data (%s)', addr)
        return 0

    @validate(addr=int, val=int)
    def write_byte(self, addr, val):
        """write_byte(addr, val)

        Perform SMBus Write Byte transaction.
        """
        self.logger.info('Write byte (%s, %s, %s)', addr, cmd, val)

    @validate(addr=int, cmd=int)
    def read_byte_data(self, addr, cmd):
        """read_byte_data(addr, cmd) -> result

        Perform SMBus Read Byte Data transaction.
        """
        self.logger.info('Read byte data (%s, %s)', addr, cmd)
        return 0

    @validate(addr=int, cmd=int, val=int)
    def write_byte_data(self, addr, cmd, val):
        """write_byte_data(addr, cmd, val)

        Perform SMBus Write Byte Data transaction.
        """
        self.logger.info('Write byte data (%s, %s, %s)', addr, cmd, val)

    @validate(addr=int, cmd=int)
    def read_word_data(self, addr, cmd):
        """read_word_data(addr, cmd) -> result

        Perform SMBus Read Word Data transaction.
        """
        self.logger.info('Read word data (%s, %s)', addr, cmd)
        return 0

    @validate(addr=int, cmd=int, val=int)
    def write_word_data(self, addr, cmd, val):
        """write_word_data(addr, cmd, val)

        Perform SMBus Write Word Data transaction.
        """
        self.logger.info('Write word data (%s, %s, %s)', addr, cmd, vals)

    @validate(addr=int, cmd=int, val=int)
    def process_call(self, addr, cmd, val):
        """process_call(addr, cmd, val)

        Perform SMBus Process Call transaction.

        Note: although i2c_smbus_process_call returns a value, according to
        smbusmodule.c this method does not return a value by default.

        Set _compat = False on the SMBus instance to get a return value.
        """
        self.logger.info('Process call (%s, %s, %s)', addr, cmd, val)

    @validate(addr=int, cmd=int)
    def read_block_data(self, addr, cmd):
        """read_block_data(addr, cmd) -> results

        Perform SMBus Read Block Data transaction.
        """
        # XXX untested, the raspberry pi i2c driver does not support this
        # command
        self.logger.info('Read block data (%s, %s)', addr, cmd)
        return 0

    @validate(addr=int, cmd=int, vals=list)
    def write_block_data(self, addr, cmd, vals):
        """write_block_data(addr, cmd, vals)

        Perform SMBus Write Block Data transaction.
        """
        self.logger.info('Write block data (%s, %s, %s)', addr, cmd, vals)

    @validate(addr=int, cmd=int, vals=list)
    def block_process_call(self, addr, cmd, vals):
        """block_process_call(addr, cmd, vals) -> results

        Perform SMBus Block Process Call transaction.
        """
        self.logger.info('Block process call (%s, %s, %s)', addr, cmd, vals)

    @validate(addr=int, cmd=int, len=int)
    def read_i2c_block_data(self, addr, cmd, len=32):
        """read_i2c_block_data(addr, cmd, len=32) -> results

        Perform I2C Block Read transaction.
        """
        self.logger.info('I2C read block data (%s, %s, %s)', addr, cmd, len)
        return 0

    @validate(addr=int, cmd=int, vals=list)
    def write_i2c_block_data(self, addr, cmd, vals):
        """write_i2c_block_data(addr, cmd, vals)

        Perform I2C Block Write transaction.
        """
        self.logger.info('I2C Write block data (%s, %s, %s)', add, cmd, vals)

    @property
    def pec(self):
        return self._pec

    @pec.setter
    def pec(self, value):
        """True if Packet Error Codes (PEC) are enabled"""
        self.logger.info('Attempting to check PEC %s', value)


def smbus_data_to_list(data):
    block = data.block
    return [block[i + 1] for i in range(block[0])]


def list_to_smbus_data(data, vals):
    block_max = SMBUS.I2C_SMBUS_BLOCK_MAX
    if len(vals) > block_max or len(vals) == 0:
        raise OverflowError("Third argument must be a list of at least one, "
                            "but not more than %d integers" % block_max)
    data.block[0] = len(vals)
    for i, val in enumerate(vals):
        data.block[i + 1] = val
