#!/usr/bin/python3

from distutils.core import setup

setup(
    name='PPA Extender',
    version='0.0.1',
    author='Mirko Brombin',
    description='Easily manage PPA',
    url='https://github.com/mirkobrombin/ppaextender',
    license='GNU GPL3',
    scripts=['com.github.mirkobrombin.ppaextender'],
    packages=['ppaextender'],
    data_files=[('share/metainfo', ['data/com.github.mirkobrombin.ppaextender.appdata.xml']),
                ('share/applications', ['data/com.github.mirkobrombin.ppaextender.desktop']),
                ('share/icons/hicolor/128x128/apps',['data/com.github.mirkobrombin.ppaextender.svg']),
                ('share/ppaextender',['data/style.css']),
                ('lib/ppaextender',['pkexec']),
    ],
)
