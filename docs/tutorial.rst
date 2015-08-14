Tutorial
========

This tutorial is intended as an introduction to working with
**HPLeftHandClient**.

Prerequisites
-------------
Before we start, make sure that you have the **HPLeftHandClient** distribution
:doc:`installed <installation>`. In the Python shell, the following
should run without raising an exception:

.. code-block:: bash

  >>> import hplefthandclient

This tutorial also assumes that a LeftHand array is up and running and the
LeftHand OS is running.

Create the Client and login
---------------------------
The first step when working with **HPLeftHandClient** is to create a
:class:`~hplefthandclient.client.HPLeftHandClient` to the LeftHand drive array
and logging in to create the session.   You must :meth:`~hplefthandclient.client.HPLeftHandClient.login` prior to calling the other APIs to do work on the LeftHand.
Doing so is easy:

.. code-block:: python

  from hplefthandclient import client, exceptions
  #this creates the client object and sets the url to the
  #LeftHand server with IP 10.10.10.10 on port 8008.
  cl = client.HPLeftHandClient("https://10.10.10.10:8008/api/v1")

  try:
      cl.login(username, password)
      print "Login worked!"
  except exceptions.HTTPUnauthorized as ex:
      print "Login failed."

When you are done with the the client, it's a good idea to logout from
the LeftHand so there isn't a stale session sitting around.

.. code-block:: python

   cl.logout()
   print "logout worked"

Getting a list of Volumes
-------------------------
After you have logged in, you can start making calls to the LeftHand APIs.
A simple example is getting a list of existing volumes on the array with
a call to :meth:`~hplefthandclient.client.HPLeftHandClient.getVolumes`.

.. code-block:: python

    import pprint
    try:
       volumes = cl.getVolumes()
       pprint.pprint(volumes)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       #something unexpected happened
       print ex


.. note:: volumes is an array of volumes in the above call

