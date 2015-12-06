# -*- coding: utf-8 -*-
__author__ = 'alsbi'

class Error_update_domain(Exception):
    def __init__(self, message=None, error_code=0):
        super(Error_update_domain, self).__init__(message)
        self.message = message
