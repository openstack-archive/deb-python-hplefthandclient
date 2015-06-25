HP LeftHand/StoreVirtual REST Client
===================
This is a Client library that can talk to the HP LeftHand/StoreVirtual Storage array.
The HP LeftHand storage array has a REST web service interface.
This client library implements a simple interface to talk with that REST
interface using the python Requests http library.

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
* Get Cluster(s)
* Get Cluster by Name
* Get Server(s)
* Get Server by Name
* Create Server
* Delete Server
* Add Server Access
* Remove Server Access


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

To run all unit tests with code coverage::

 $ tox -e cover

The output of the coverage tests will be placed into the ``coverage`` dir.

Folders
=======

* docs -- contains the documentation.
* hplefthandlient -- the actual client.py library
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

  $ python test/HPLeftHandMockServer_flask.py -port 5001 -user <USERNAME> -password <PASSWORD> -debug
