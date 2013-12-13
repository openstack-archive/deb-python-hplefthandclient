Installing / Upgrading
======================
.. highlight:: bash

**HPLeftHandClient** is in the `Python Package Index
<http://pypi.python.org/pypi/hplefthandclient/>`_.

Installing with pip
-------------------

We prefer `pip <http://pypi.python.org/pypi/pip>`_
to install hplefthandclient on platforms other than Windows::

  $ pip install hplefthandclient

To upgrade using pip::

  $ pip install --upgrade hplefthandclient

Installing with easy_install
----------------------------

If you must install hplefthandclient using
`setuptools <http://pypi.python.org/pypi/setuptools>`_ do::

  $ easy_install hplefthandclient

To upgrade do::

  $ easy_install -U hplefthandclient


Installing from source
----------------------

If you'd rather install directly from the source (i.e. to stay on the
bleeding edge), install the C extension dependencies then check out the
latest source from github and install the driver from the resulting tree::

  $ git clone git://github.com/WaltHP/python-lefthandlient.git
  $ cd python-lefthandclient/
  $ python setup.py install

