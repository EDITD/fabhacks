# Fabhacks
# File: setup.py
# Desc: needed

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    version='0.1.5',
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