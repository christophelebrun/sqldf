#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setup(name='sqldf',
 
      version='0.4.2',
 
      url='https://github.com/christophelebrun/sqldf',
 
      license='MIT',
 
      author='Christophe Lebrun',
 
      author_email='lebr1.christophe@gmail.com',
 
      description='A simple way to run SQL queries (SQLite3) on pandas.Dataframe objects.',

      packages=['sqldf'],
 
      long_description=long_description,
      
      long_description_content_type="text/markdown",
 
      zip_safe=False,
 
      setup_requires=['pandas>=1.0'],
 
      test_suite='pandas')
