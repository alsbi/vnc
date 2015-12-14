# -*- coding: utf-8 -*-
__author__ = 'alsbi'

from threading import Thread

import websockify


class Proxy(websockify.websocketproxy.WebSocketProxy):
    port = {}

    @classmethod
    def get_port(cls, uuid):
        if uuid in Proxy.port:
            return Proxy.port[uuid]
        port = list(set(range(50000, 63000)) - set([port for port in Proxy.port]))[0]
        Proxy.port[uuid] = port
        return port

    def __init__(self, *args, target_host=None, target_port=None, listen_host=None, uuid=None):
        self.target_host = target_host
        self.target_port = target_port
        self.listen_host = listen_host
        self.listen_port = Proxy.get_port(uuid = uuid)
        super(Proxy, self).__init__(*args, **self.__dict__)
        self.uuid = uuid

    def start(self):
        self.run_once = True
        return self.start_server


class Worker(Thread):
    def __init__(self, manager, task):
        Thread.__init__(self)
        self.manager = manager
        self.task = task
        self.start()

    def run(self):
        try:
            self.task.start()
        except Exception as e:
            self.manager.delete(self.task.uuid)


class ProxyManager():
    def __init__(self, listen_host):
        self.listen_host = listen_host
        self.list_proxy = {}
        pass

    def create(self, uuid, port, host):
        proxy = Proxy(target_port = port, target_host = host, listen_host = self.listen_host)
        self.list_proxy[uuid] = proxy
        Worker(self, proxy).run()
        return proxy

    def exist(self, uuid):
        if uuid in self.list_proxy:
            return True
        else:
            return False

    def delete(self, uuid):
        del self.list_proxy[uuid]
