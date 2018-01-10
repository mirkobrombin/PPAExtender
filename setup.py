#!/usr/bin/python3

from distutils.core import setup

setup(
    name='Repoman',
    version='0.0.6',
    author='Ian Santopietro',
    description='Easily manage PPAs',
    url='https://github.com/isantop/repoman',
    license='GNU GPL3',
    scripts=['xyz.isantop.repoman'],
    packages=['repoman'],
    data_files=[
        ('share/metainfo', ['data/xyz.isantop.repoman.appdata.xml']),
        ('share/applications', ['data/xyz.isantop.repoman.desktop']),
        ('share/repoman', ['data/style.css']),
        ('share/repoman', ['po']),
        ('lib/repoman', ['xyz.isantop.repoman.pkexec']),
    ],
)
