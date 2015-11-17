Tutorial
========

This tutorial is intended as an introduction to working with
**HPELeftHandClient**.

Prerequisites
-------------
Before we start, make sure that you have the **HPELeftHandClient** distribution
:doc:`installed <installation>`. In the Python shell, the following
should run without raising an exception:

.. code-block:: bash

  >>> import hpelefthandclient

This tutorial also assumes that a LeftHand array is up and running and the
LeftHand OS is running.

Create the Client and login
---------------------------
The first step when working with **HPELeftHandClient** is to create a
:class:`~hpelefthandclient.client.HPELeftHandClient` to the LeftHand drive array
and logging in to create the session.   You must :meth:`~hpelefthandclient.client.HPELeftHandClient.login` prior to calling the other APIs to do work on the LeftHand.
Doing so is easy:

.. code-block:: python

  from hpelefthandclient import client, exceptions
  #this creates the client object and sets the url to the
  #LeftHand server with IP 10.10.10.10 on port 8081.
  cl = client.HPELeftHandClient("https://10.10.10.10:8081/lhos")

  # SSL certification verification is defaulted to False. In order to
  # override this, set secure=True. or secure='/path/to/cert.crt'
  # cl = client.HPELeftHandClient("https://10.10.10.10:8081/lhos",
  #                                secure=True)
  # Or, to use ca certificates as documented by Python Requests,
  # pass in the ca-certificates.crt file
  # http://docs.python-requests.org/en/v1.0.4/user/advanced
  # cl = client.HPELeftHandClient("https://10.10.10.10:8081/lhos",
  #                                secure='/etc/ssl/certs/ca-certificates.crt')

  # Set the SSH authentication options for the SSH based calls.
  cl.setSSHOptions(ip_address, username, password)

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
a call to :meth:`~hpelefthandclient.client.HPELeftHandClient.getVolumes`.

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

