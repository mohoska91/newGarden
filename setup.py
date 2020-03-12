import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    requirements = f.read().splitlines()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    version = f.read()

setup(
    name='newGarden',
    version=version,
    scripts=['bin/gpioserver', 'bin/gardenserver', 'bin/gardening'],
    packages=find_packages('newGarden'),
    package_dir={"": "newGarden"},
    url='',
    license='',
    install_requires=requirements,
    long_description=long_description,
    author='Peter Mohos',
    author_email='mohos.peter91@gmail.com',
    description='Wardrobe garden'
)
