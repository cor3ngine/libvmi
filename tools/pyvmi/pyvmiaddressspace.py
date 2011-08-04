# Volatility
# Copyright (C) 2011 Sandia National Laboratories
#
# Authors:
# bpayne@sandia.gov (Bryan D. Payne)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details. 
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA 
#

""" These are standard address spaces supported by Volatility """
import volatility.addrspace as addrspace
import pyvmi

#pylint: disable-msg=C0111

class PyVmiAddressSpace(addrspace.BaseAddressSpace):
    """
    This address space can be used in conjunction with LibVMI
    and the Python bindings for LibVMI.  The end result is that
    you can connect Volatility to view the memory of a running
    virtual machine from any virtualization platform that
    LibVMI supports.

    For this AS to be instantiated, we need the VM name to
    connect to.
    """

    order = 90
    def __init__(self, base, config, layered = False, **kwargs):
        self.as_assert(base == None or layered, 'Must be first Address Space')
        addrspace.BaseAddressSpace.__init__(self, base, config, **kwargs)
        self.vmname = config.LOCATION
        self.vmi = pyvmi.init(self.vmname, "partial")
        self.as_assert(not self.vmi is None, 'VM must be specified and running')
        self.dtb = self.get_cr3()

    def read(self, addr, length):
        return self.vmi.read_pa(addr, length)

    def is_valid_address(self, addr):
        if addr == None:
            return False
        return addr < self.vmi.get_memsize() - 1

    def write(self, addr, data):
        nbytes = self.vmi.write_pa(addr, data)
        if nbytes != len(data):
            return False
        return True

    def get_cr3(self):
        return self.vmi.get_vcpureg("cr3", 0);