========================
Team and repository tags
========================

.. image:: http://governance.openstack.org/badges/deb-python-hplefthandclient.svg
    :target: http://governance.openstack.org/reference/tags/index.html

.. Change things from this point on

.. image:: https://img.shields.io/pypi/v/python-lefthandclient.svg
    :target: https://pypi.python.org/pypi/python-lefthandclient/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/python-lefthandclient.svg
    :target: https://pypi.python.org/pypi/python-lefthandclient/
    :alt: Downloads

HPE LeftHand/StoreVirtual REST Client
=====================================
This is a Client library that can talk to the HPE LeftHand/StoreVirtual Storage array.
The HPE LeftHand storage array has a REST web service interface as well as runs SSH.
This client library implements a simple interface to talk with that REST
interface using the python Requests http library and communicates via SSH using
Pytohn's paramiko library.

This is the new location for the rebranded HP LeftHand/StoreVirtual REST Client and
will be where all future releases are made. It was previously located on PyPi at:
https://pypi.python.org/pypi/hplefthandclient

The GitHub repository for the old HP LeftHand/StoreVirtual REST Client is located at:
https://github.com/hpe-storage/python-lefthandclient/tree/1.x

The HP LeftHand/StoreVirtual REST Client (hplefthandclient) is now considered deprecated.

Requirements
============
This branch requires 11.5 version or later of the LeftHand OS firmware.

Capabilities
============
* Get Volume(s)
* Get Volume by Name
* Create Volume
* Delete Volume
* Modify Volume
* Clone Volume
* Get Snapshot(s)
* Delete Shapshot
* Get Shapshot by Name
* Create Snapshot
* Delete Snapshot
* Clone Snapshot
* Modify Snapshot
* Get Cluster(s)
* Get Cluster by Name
* Get Server(s)
* Get Server by Name
* Create Server
* Delete Server
* Add Server Access
* Remove Server Access
* Make Volume Remote
* Make Volume Primary
* Create Remote Snapshot Schedule
* Delete Remote Snapshot Schedule
* Query Remote Snapshot Schedule
* Stop Remote Snapshot Schedule
* Start Remote Snapshot Schedule


Installation
============

To install::

 $ sudo pip install .


Unit Tests
==========

To run all unit tests::

 $ tox -e py27

To run a specific test::

 $ tox -e py27 -- test/file.py:class_name.test_method_name

To run all unit tests with Python 3.4::

 $ tox -e py34

To run a specific test with Python 3.4::

 $ tox -e py34 -- test/file.py:class_name.test_method_name

To run all unit tests with code coverage::

 $ tox -e cover

The output of the coverage tests will be placed into the ``coverage`` dir.

Folders
=======

* docs -- contains the documentation.
* hpelefthandlient -- the actual client.py library
* test -- unit tests
* samples -- some sample uses


Documentation
=============

To build the documentation::

 $ tox -e docs

To view the built documentation point your browser to::

  docs/html/index.html


Running Simulators
==================

Manually run flask server (when config.ini unit=true)::

* WSAPI::

  $ python test/HPELeftHandMockServer_flask.py -port 5001 -user <USERNAME> -password <PASSWORD> -debug

* SSH::

  $ python test/HPELeftHandMockServer_ssh.py [port]
