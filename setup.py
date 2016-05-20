#!/usr/bin/env python

from __future__ import with_statement
import distutils.core, os

try:
    import setuptools
except ImportError:
    pass

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

distutils.core.setup(name='shiftpi',
      version="0.3",
      description="ShiftPi is the easiest way to work with 74HC595 shift registers on your Raspberry Pi.",
      author='Gwilyn Saunders',
      author_email='gwilyn.saunders@mk2es.com.au',
      url='https://git.gwillz.com.au/mk2/shiftpi',
      packages=['shiftpi'],
      long_description=read('README.md'),
      classifiers=[
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Shells',
          'Topic :: Utilities',
          ],
     )
