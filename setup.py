# -*- coding: utf-8 -*-
# Copyright (c) 2008-2013 Michael Howitz
# See also LICENSE.txt

import os.path
import setuptools

def read(*path_elements):
    return file(os.path.join(*path_elements)).read()

version = '1.10.0'
long_description = '\n\n'.join([read('README.rst'),
                                read('CHANGES.rst')])

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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Paste',
        'Framework :: Zope3',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        ],
    packages=setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages = ['icemac', 'icemac.ab'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gocept.cache',
        'icemac.ab.locales >= 0.8',
        'icemac.addressbook >= 1.10.0.dev0',
        'icemac.truncatetext >= 0.2',
        'pytz',
        'setuptools',
        'z3c.wizard',
        'zc.sourcefactory',
        'zope.container',
        'zope.generations',
        'zope.interface',
        'zope.schema',
        ],
    extras_require = dict(
        test=[
            'icemac.addressbook [test]',
            'zope.testing >= 3.8.0',
            'zope.traversing',
            ]),
    )
