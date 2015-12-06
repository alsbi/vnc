# -*- coding: utf-8 -*-
__author__ = 'alsbi'

import sys
from collections import OrderedDict


import libvirt

from vnc_viewer.virshlike.tools import utils
from vnc_viewer.config import *


class Connector(object):
    def __init__(self, login=None, password=None, host=None):
        self.__login = login
        self.__pass = password
        self.__host = host

    def connect(self):
        def request_cred(credentials, user_data):
            for credential in credentials:
                if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                    credential[4] = self.__login
                elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                    credential[4] = self.__pass
            return 0

        auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], request_cred, None]
        conn = libvirt.openAuth('qemu+tcp://{host}/system'.format(host = self.__host), auth, 0)

        if conn == None:
            print('Failed to open connection to qemu+tcp://{host}/system'.format(host=self.__host), file = sys.stderr)
            exit(1)
        return conn

class Manager(object):
    def __init__(self):
        self.login = SASL_USER
        self.password = SASL_PASS
        self.host = HOST_LOCAL_VIRSH
        self.conn = Connector(login = self.login, password = self.password, host = self.host).connect()

    def status(self):
        return OrderedDict([
            ('hostname', self.conn.getHostname()),
            ('memory usage', '\n'.join(["{key}:{value}".format(key = key, value = memory) for key, memory in
                                        self.conn.getMemoryParameters().items()])),
            ('all domain', len(self.conn.listAllDomains())),
            ('started domain', len(self.get_active_domain()))
        ])

    def start_domain(self, uuid):
        try:
            domain = self.conn.lookupByUUIDString(uuid)
            if not domain.isActive():
                return self.conn.lookupByUUIDString(uuid).create()
        except libvirt.libvirtError as e:
            print(e)

    def stop_domain(self, uuid):
        try:
            domain = self.conn.lookupByUUIDString(uuid)
            if domain.isActive():
                return domain.destroy()
        except libvirt.libvirtError as e:
            print(e)

    def shutdown_domain(self, uuid):
        try:
            domain = self.conn.lookupByUUIDString(uuid)
            if domain.isActive():
                return domain.shutdown()
        except libvirt.libvirtError as e:
            print(e)

    def restart_domain(self, uuid):
        try:
            domain = self.conn.lookupByUUIDString(uuid)
            if domain.isActive():
                return domain.reboot()
        except libvirt.libvirtError as e:
            print(e)

    def reset_domain(self, uuid):
        try:
            domain = self.conn.lookupByUUIDString(uuid)
            if domain.isActive():
                return domain.reset()
        except libvirt.libvirtError as e:
            print(e)

    def get_domain_by_uuid(self, uuid):
        return self.conn.lookupByUUIDString(uuid)

    def get_active_domain(self):
        return self.conn.listAllDomains(5)

    def get_inactive_domain(self):
        return self.conn.listAllDomains(2)

    def get_all_domain(self):
        return self.conn.listAllDomains()

    def get_vnc_port_by_uuid(self, uuid):
        return utils.vnc_port(self.get_domain_by_uuid(uuid = uuid))

    def set_vnc_pass_by_uuid(self, uuid):
        return utils.set_vnc_passwd(self.get_domain_by_uuid(uuid = uuid))

    def __del__(self):
        self.conn.close()
