#!/usr/bin/python3

import glob, os
from distutils.core import setup

install_data = [('share/metainfo', ['data/xyz.isantop.repoman.appdata.xml']),
                ('share/applications', ['data/xyz.isantop.repoman.desktop']),
                ('bin/repoman',['data/style.css']),
                ('bin/repoman',['repoman/constants.py']),
                ('bin/repoman',['repoman/detail.py']),
                ('bin/repoman',['repoman/headerbar.py']),
                ('bin/repoman',['repoman/helper.py']),
                ('bin/repoman',['repoman/list.py']),
                ('bin/repoman',['repoman/main.py']),
                ('bin/repoman',['repoman/ppa.py']),
                ('bin/repoman',['repoman/stack.py']),
                ('bin/repoman',['repoman/welcome.py']),
                ('bin/repoman',['repoman/window.py']),
                ('bin/repoman',['repoman/__init__.py']),
                ('bin/repoman',['pkexec'])]

setup(  name='Repoman',
        version='0.0.1',
        author='Ian Santopietro',
        description='Easily manage PPA',
        url='https://github.com/isantop/repoman',
        license='GNU GPL3',
        scripts=['xyz.isantop.repoman'],
        packages=['repoman'],
        data_files=install_data)
