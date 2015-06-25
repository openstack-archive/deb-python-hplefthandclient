import hplefthandclient

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
import sys


setup(
  name='hplefthandclient',
  version=hplefthandclient.version,
  description="HP LeftHand/StoreVirtual HTTP REST Client",
  author="Kurt Martin",
  author_email="kurt.f.martin@hp.com",
  maintainer="Kurt Martin",
  keywords=["hp", "lefthand", "storevirtual", "rest"],
  requires=['requests'],
  install_requires=['requests'],
  tests_require=["nose", "nose-testconfig", "flask", "Werkzeug", "flake8"],
  license="Apache License, Version 2.0",
  packages=find_packages(),
  provides=['hplefthandclient'],
  url="http://packages.python.org/hplefthandclient",
  classifiers=[
     'Development Status :: 3 - Alpha',
     'Intended Audience :: Developers',
     'License :: OSI Approved :: Apache Software License',
     'Environment :: Web Environment',
     'Programming Language :: Python',
     'Programming Language :: Python :: 2.6',
     'Programming Language :: Python :: 2.7',
     'Programming Language :: Python :: 3.4',
     'Topic :: Internet :: WWW/HTTP',
     ]
  )
