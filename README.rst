HP LeftHand/StoreVirtual REST Client
===================
This is a Client library that can talk to the HP LeftHand/StoreVirtual Storage array.
The HP LeftHand storage array has a REST web service interface.
This client library implements a simple interface to talk with that REST
interface using the python httplib2 http library.

Requirements
============
This branch requires 11.5 version of the LeftHand OS firmware.

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

::

 $ python setup.py install


Unit Tests
==========

::

 $ pip install nose
 $ pip install nose-testconfig
 $ cd test
 $ nosetests --tc-file config.ini


Folders
=======
* docs -- contains the documentation.
* hplefthandlient -- the actual client.py library
* test -- unit tests
* samples -- some sample uses


Documentation
=============

To view the built documentation point your browser to

::

  python-hplefthand/docs/_build/html/index.html



