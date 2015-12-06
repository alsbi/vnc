# -*- coding: utf-8 -*-
__author__ = 'alsbi'
from xml.dom import minidom
from xml.etree import ElementTree as ET
import string
from random import *

from libvirt import libvirtError
from vnc_viewer.errors import *


class utils(object):
    @staticmethod
    def vnc_port(domain):
        xml = minidom.parseString(domain.XMLDesc(0))
        domainTypes = xml.getElementsByTagName('graphics')
        for domainType in domainTypes:
            port = (domainType.getAttribute('websocket'))
            if port:
                return port

        raise KeyError

    @staticmethod
    def set_vnc_passwd(domain):
        passwd = pass_gen()
        xml = ET.fromstring(domain.XMLDesc(0))
        graphic_element = xml.find('.//graphics')
        graphic_element.attrib['passwd'] = passwd
        try:
            domain.updateDeviceFlags(str(ET.tostring(graphic_element).decode("utf-8")), 0)
        except libvirtError as e:
            raise Error_update_domain(e)
        return passwd


def pass_gen():
    characters = string.ascii_letters + string.digits
    password = "".join(choice(characters) for x in range(randint(8, 16)))
    return str(password)
