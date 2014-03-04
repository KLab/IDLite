#!/usr/bin/python
from setuptools import setup, find_packages

setup(name="idlite",
      version="0.0.2",
      packages=find_packages(),
      scripts=['bin/idlite'],
      install_requires=['PLY'],
      classifiers=[
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 2.7"],
      )
