# -*- coding: utf-8 -*-
__author__ = 'alsbi'

import os

from flask import Flask, render_template, send_from_directory, session, request, redirect, url_for

from ..virshlike import Manager
from vnc_viewer.engine.errors import *
from ..config import *

tmpl_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'templates')
app = Flask(__name__, static_url_path = '{template}/static'.format(template = tmpl_dir), template_folder = tmpl_dir)
app.secret_key = SECRET_KEY_APP
mn = Manager()


@app.route('/')
@app.route('/consoles')
def get_domain_list():
    if 'username' in session:
        return render_template('consoles.html', domain_list = mn.get_active_domain(), info = mn.status(),
                               domain_list_inactive = mn.get_inactive_domain())
    else:
        return redirect(url_for('login'))

@app.route('/console/<vm_name>')
def get_domain_by_uid(vm_name):
    if 'username' in session:
        try:
            return render_template('console.html', domain_list = mn.get_active_domain(), id = vm_name,
                                   domain_list_inactive = mn.get_inactive_domain(), host = HOST_REMOTE_VIRSH,
                                   port = mn.get_vnc_port_by_uuid(vm_name),
                                   password = mn.set_vnc_pass_by_uuid(vm_name))
        except Error_update_domain as e:
            if not mn.get_domain_by_uuid(vm_name).isActive():
                return "<div style='background-color:white'>Connection lost</div>"
            return repr(e)
    else:
        return redirect(url_for('login'))


@app.route('/console/<vm_name>/<action>')
def action_domain_by_uid(vm_name, action):
    if 'username' in session:
        if action in ['stop', 'start', 'reboot', 'shutdown', 'reset']:
            getattr(mn, '%s_domain' % action)(vm_name)
        try:
            return redirect(url_for('get_domain_by_uid', vm_name = vm_name, host = HOST_REMOTE_VIRSH,
                                port = mn.get_vnc_port_by_uuid(vm_name),
                                password = mn.set_vnc_pass_by_uuid(vm_name)))
        except Error_update_domain as e:
                if not mn.get_domain_by_uuid(vm_name).isActive():
                    return "<div style='background-color:white'>Connection lost</div>"
                return repr(e)
    else:
        return redirect(url_for('login'))


# debug
@app.route('/view/<vm_name>/<path:path>')
def get_static(vm_name, path):
    if 'username' in session:
        return send_from_directory('static', path)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if LOGINS.get(request.form['username']) == request.form['password']:
            session['username'] = request.form['username']
            return redirect(url_for('get_domain_list'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


def start():
    app.run(debug = True, host = '0.0.0.0')
