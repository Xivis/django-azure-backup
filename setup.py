import os
from setuptools import find_packages, setup
import django_azure_backup as app


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()
    except IOError:
        return u''

setup(
    name='django_azure_backup',
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.md'),
    license='The MIT License',
    platforms=['OS Independent'],
    url='https://www.xivis.com/',
    author='Ramiro Gonzalez',
    author_email='ramiro@xivis.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split('\n'),
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python', ],
)
