# -*- coding: utf-8 -*-
import os.path
import setuptools


def read(*path_elements):
    """Read a path."""
    return open(os.path.join(*path_elements)).read()

version = '2.13.dev0'
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
    url='https://pypi.org/project/icemac.ab.importer',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['icemac', 'icemac.ab'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'gocept.cache',
        'grokcore.component',
        'icemac.ab.locales >= 0.8',
        'icemac.addressbook >= 9.5.dev0',
        'icemac.truncatetext >= 0.2',
        'pytz',
        'setuptools',
        'six',
        'z3c.wizard',
        'zc.sourcefactory',
        'zope.container',
        'zope.generations',
        'zope.interface',
        'zope.schema',
        'zope.securitypolicy >= 4.1',
    ],
    extras_require=dict(
        test=[
            'icemac.addressbook [test]',
            'zope.testing >= 3.8.0',
            'zope.traversing',
        ]),
)
