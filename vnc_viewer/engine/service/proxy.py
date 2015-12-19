# -*- coding: utf-8 -*-
__author__ = 'alsbi'

from multiprocessing import Process

from websockify import WebSocketProxy


class Proxy():
    port = {}

    @classmethod
    def get_port(cls,
                 uuid):
        if uuid in Proxy.port:
            return Proxy.port[uuid]
        port = list(set(range(50000, 63000)) - set([port for port in Proxy.port.values()]))[0]
        Proxy.port[uuid] = port
        return port

    def __init__(self,
                 target_host=None,
                 target_port=None,
                 listen_host=None,
                 uuid=None):
        self.target_host = target_host
        self.target_port = target_port
        self.listen_host = listen_host
        self.listen_port = Proxy.get_port(uuid = uuid)
        self.uuid = uuid

    def start_proxy(self):
        def run():
            cert = '/home/vnc/vnc_service/bin/server.crt'
            key = '/home/vnc/vnc_service/bin/server.key'
            params = {'ssl_only': True,
                      'cert': cert,
                      'key': key,
                      'target_port': self.target_port}
            server = WebSocketProxy(**params)
            server.start_server()

        proc = Process(target = run)
        proc.start()
        return proc


class ProxyManager(object):
    def __init__(self,
                 listen_host=None,
                 target_host=None):
        self.listen_host = listen_host
        self.target_host = target_host
        self.list_proxy = {}

    def create(self,
               uuid=None,
               port=None):
        if not self.list_proxy.get(uuid):
            proxy = Proxy(target_port = port,
                          target_host = self.target_host,
                          listen_host = self.listen_host,
                          uuid = uuid)
            self.list_proxy[uuid] = proxy
            proxy.start_proxy()
            return proxy
        else:
            return self.list_proxy[uuid]

    def delete(self, uuid):
        if self.list_proxy.get(uuid):
            del self.list_proxy[uuid]
