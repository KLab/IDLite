#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(name="idlite",
      version="0.0.2",
      packages=find_packages(),
      scripts=['bin/idlite'],
      install_requires=['PLY'],
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 2.7",
      ],
      )
