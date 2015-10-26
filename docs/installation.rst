Installing / Upgrading
======================
.. highlight:: bash

**HPELeftHandClient** is in the `Python Package Index
<http://pypi.python.org/pypi/python-lefthandclient/>`_.

Installing with pip
-------------------

We prefer `pip <http://pypi.python.org/pypi/pip>`_
to install hpelefthandclient on platforms other than Windows::

  $ pip install python-lefthandclient

To upgrade using pip::

  $ pip install --upgrade python-lefthandclient

Installing with easy_install
----------------------------

If you must install hpelefthandclient using
`setuptools <http://pypi.python.org/pypi/setuptools>`_ do::

  $ easy_install python-lefthandclient

To upgrade do::

  $ easy_install -U python-lefthandclient


Installing from source
----------------------

If you'd rather install directly from the source (i.e. to stay on the
bleeding edge), install the C extension dependencies then check out the
latest source from github and install the driver from the resulting tree::

  $ git clone git://github.com/hpe-storage/python-lefthandlient.git
  $ cd python-lefthandclient/
  $ pip install .

Uninstalling an old client
--------------------------

If the older **HPLeftHandClient** was installed on the system already it
will need to be removed. Run the following command to remove it::

  $ sudo pip uninstall hplefthandclient
