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
