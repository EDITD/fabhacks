# Fabhacks
# File: setup.py
# Desc: needed

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSIONS = {
    'crawl_docs': '0.0.5'
}

setup(
    version='0.1.0',
    name='Fabhacks',
    description='Some Fabric-based hacks',
    author='Nick @ EDITD',
    author_email='dev@editd.com',
    url='http://github.com/EDITD/fabhacks',
    package_dir={ 'fabhacks': 'fabhacks' },
    install_requires=[
        'fabric>=1.8.0'
    ],
    packages=[
        'fabhacks'
    ]
)