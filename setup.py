#!/usr/bin/env python

from setuptools import setup
import os

requirements = [i for i in open('requirements.txt').read().split() if 'git' not in i]

def get_long_description(fname):
    try:
        import pypandoc
        return pypandoc.convert(fname, 'rst')
    except:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='shiftpi',
      version="0.3.3",
      description="ShiftPi is the easiest way to work with 74HC595 shift registers on your Raspberry Pi.",
      author='Gwilyn Saunders',
      author_email='gwilyn.saunders@mk2es.com.au',
      url='https://git.gwillz.com.au/mk2/shiftpi',
      packages=['shiftpi'],
#      install_requires=requirements,
      long_description=get_long_description('README.md'),
      classifiers=[
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Shells',
          'Topic :: Utilities',
          ],
     )
