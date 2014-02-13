from setuptools import setup, find_packages
import sys, os

version = '0.1'
requires = [
    'requests',
    'httmock',
    'nose',
    'coverage'
]

setup(name='pyenketo',
      version=version,
      description="Python bindings for the Enketo API",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python enketo onaio',
      author='Ona Labs',
      author_email='lweya@ona.io',
      url='',
      license='MIT',
      test_suite='pyenketo',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
