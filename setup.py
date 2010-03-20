# -*- coding: utf-8 -*-
# Copyright (c) 2008-2010 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return "\n\n" + file(os.path.join(*path_elements)).read()

version = '1.3.0'
long_description = (
    read('README.txt') +
    read('CHANGES.txt')
    )

setuptools.setup(
    name='icemac.ab.importer',
    version=version,
    description="Import infrastructure for icemac.addressbook",
    long_description=long_description,
    keywords='icemac.addressbook',
    author='Michael Howitz',
    author_email='icemac@gmx.net',
    url='http://pypi.python.org/pypi/icemac.ab.importer',
    license='ZPL 2.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Framework :: Zope3',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        ],
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['icemac', 'icemac.ab'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gocept.cache',
        'icemac.addressbook > 1.2.0',
        'icemac.truncatetext >= 0.2',
        'icemac.ab.locales >= 0.2',
        'pytz',
        'setuptools',
        'z3c.wizard',
        'zc.sourcefactory',
        'zope.container',
        'zope.interface',
        'zope.schema',
        'zope.app.generations',
        ],
    extras_require = dict(
        test=[
            'icemac.addressbook [test]',
            'zope.app.testing',
            'zope.testing >= 3.8.0',
            'zope.traversing',
            ]),
    )
