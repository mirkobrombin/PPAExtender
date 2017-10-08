#!/usr/bin/python3

import glob, os 
from distutils.core import setup

install_data = [('share/applications', ['data/com.github.mirkobrombin.ppaextender.desktop']),
                ('share/metainfo', ['data/com.github.mirkobrombin.ppaextender.appdata.xml']),
                ('share/icons/hicolor/128x128/apps',['data/com.github.mirkobrombin.ppaextender.svg']),
                ('bin/ppaextender',['ppaextender/constants.py']),
                ('bin/ppaextender',['ppaextender/detail.py']),
                ('bin/ppaextender',['ppaextender/headerbar.py']),
                ('bin/ppaextender',['ppaextender/helper.py']),
                ('bin/ppaextender',['ppaextender/list.py']),
                ('bin/ppaextender',['ppaextender/main.py']),
                ('bin/ppaextender',['ppaextender/ppa.py']),
                ('bin/ppaextender',['ppaextender/stack.py']),
                ('bin/ppaextender',['ppaextender/welcome.py']),
                ('bin/ppaextender',['ppaextender/window.py']),
                ('bin/ppaextender',['ppaextender/__init__.py'])]

setup(  name='PPA Extender',
        version='0.0.1',
        author='Mirko Brombin',
        description='Easily manage PPA',
        url='https://github.com/mirkobrombin/ppaextender',
        license='GNU GPL3',
        scripts=['com.github.mirkobrombin.ppaextender'],
        packages=['ppaextender'],
        data_files=install_data)
