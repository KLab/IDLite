#!/usr/bin/python
from setuptools import setup, find_packages

setup(name="idlite",
      version="0.0.1",
      packages=find_packages(),
      scripts=['bin/idlite'],
      install_requires=['PLY'])
