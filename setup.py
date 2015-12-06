import re
import ast

from setuptools import find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('vnc_viewer/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

from distutils.core import setup

setup(
    name = 'vnc_viewer',
    version = version,
    url = '',
    license = '',
    author = 'a.biryukov',
    include_package_data=True,
    packages = find_packages(),
    package_data = {'templates': ['*.html', 'static/*.js', 'static/*.css', 'static/*.png'],},
    author_email = 'feano4ik@gmail.com',
    description = '',
    install_requires = ['libvirt-python', 'flask'],
    entry_points = {
        'console_scripts': [
            'vnc_daemon=vnc_viewer.engine:main'
        ],
    }
)
