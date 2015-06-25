Changelog
=========


Changes in Version 1.0.0
------------------------

* First implementation of the REST API Client

Changes in Version 1.0.1
------------------------

* Updated the REST API Client to be Python 3.0 compliant

Changes in Version 1.0.2
------------------------

* Added support for query parameter in getVolume

Changes in Version 1.0.3
------------------------

* Added missing Flask imports so that running unit tests against the mock LHOS
  pass
* Added new API
   - Find Server Volumes
* Updated the mock Flask server to support server API
  calls.
* Added unit tests for server API calls.
* Added a volume unit test that makes sure that volumes are created with the
  correct size.
* Added support for PEP8 checks with tox.
* Fixed various typos in the documentation.
* Fix duplicate debug log message issue that can occur when multiple client
  objects are created.
* Updated setup.py package requirements to be consistent with the ones
  defined in requirements.txt.
* Updated setup.py package test-requirements to be consistent with the ones
  defined in test-requirements.txt.

Changes in Version 1.0.4
------------------------

* Added new API
   - Get API Version
* Fixed PEP8 violations
* Added tox environments to run tests with code coverage and to generate the documentation
* Change GitHub account reference from WaltHP to hp-storage.
* Modify the steps in the Installing from Source section to ensure correct
  installation of dependencies and ordering.
* Added tox environments to run tests with code coverage and to generate the documentation
* Consolidated the test/README.rst into the top level README.rst and added clarifications
* Added the ability for getVolumes to filter based on cluster and fields.

Changes in Version 1.0.5
------------------------

* Added improved error handling during login attempts.  Errors will now be
  more descriptive in why a login failed.

Changes in Version 1.0.6
------------------------

* Python3.4+ compliant
* Added requirements-py3.txt and test-requirements-py3.txt for Python3.4 to
  pull and install from
* Updated tox to run py34 tests
* Modified basic Python calls to work with both Python2 and Python3.4
* Fixed error that was happening during client initialization when an error
  was missing a description.
* Fixes clusterId bug in createVolume (Issue #3)
* Snapshotting of multiples volumes at one time has been enabled
* Added unit test for the Exception class.
* Removed unused error property from LeftHand exceptions.

Changes in Version 1.1.0
------------------------

* Replaced all httplib2 calls with Python Request calls
* SSL certificate verification can be enabled by passing secure=True
* SSL certificate verification can be done against a self provided .crt file
  with secure='/path/to/ca-certificates.crt'
