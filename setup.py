#!/usr/bin/env python

from distutils.core import setup

LONG_DESCRIPTION = \
'''Generate the COG website'''


setup(
    name='coglabweb',
    version='0.1.0.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['coglabweb'],
    package_dir={'coglabweb': 'coglabweb'},
    entry_points={
        'console_scripts': ['coglabweb = coglabweb.main:main']
    },
    url='https://github.com/bjpop/coglabweb',
    license='LICENSE',
    description=('Generate the COG website'),
    long_description=(LONG_DESCRIPTION),
    install_requires=["jinja2==2.9.6", "pyyaml"],
)
