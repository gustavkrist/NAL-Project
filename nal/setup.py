from setuptools import setup, find_packages

setup(name='Network Analysis library',
      version='0.1',
      description='Library for NAL project',
      author='Group 8',
      packages=find_packages('nal'),
      include_package_data=True,
      install_requires=['networkx'])
