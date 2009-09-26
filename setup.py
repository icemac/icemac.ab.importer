# -*- coding: utf-8 -*-
# Copyright (c) 2008-2009 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return "\n\n" + file(os.path.join(*path_elements)).read()

version = '0.1dev'
long_description = (
    read('README.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'masterdata.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'importer.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'wizard', 'wizard.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'wizard',
         'constraints.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'wizard',
         'keywords.txt') +
    read('src', 'icemac', 'ab', 'importer', 'browser', 'wizard',
         'edgecases.txt') +
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
        'icemac.addressbook',
        'pytz',
        'setuptools',
        'z3c.wizard',
        'zc.sourcefactory',
        'zope.container',
        'zope.interface',
        'zope.schema',
        ],
    extras_require = dict(
        test=[
            'icemac.addressbook [test]',
            'zope.app.testing',
            'zope.testing >= 3.8.0',
            'zope.traversing',
            ]),
    )
