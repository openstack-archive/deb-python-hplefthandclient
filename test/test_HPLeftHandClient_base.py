# (c) Copyright 2015 Hewlett Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test base class of LeftHand Client"""

import sys
import os

import unittest
import subprocess
import time
import inspect
from testconfig import config
import datetime

from hplefthandclient import client

try:
    # For Python 3.0 and later
    from urllib.parse import urlparse
except ImportError:
    # Fall back to Python 2's urllib2
    from urlparse import urlparse

TIME = datetime.datetime.now().strftime('%H%M%S')


class HPLeftHandClientBaseTestCase(unittest.TestCase):

    cluster_id = 0
    GB_TO_BYTES = 1073741824    # Gibibytes to bytes
    MISSING_SERVER_ID = sys.maxsize
    MISSING_VOLUME_ID = -1

    user = config['TEST']['user']
    password = config['TEST']['pass']
    cluster = config['TEST']['cluster']
    flask_url = config['TEST']['flask_url']
    url_lhos = config['TEST']['lhos_url']
    debug = config['TEST']['debug'].lower() == 'true'
    unitTest = config['TEST']['unit'].lower() == 'true'
    startFlask = config['TEST']['start_flask_server'].lower() == 'true'

    def setUp(self):

        cwd = os.path.dirname(os.path.abspath(
                              inspect.getfile(inspect.currentframe())))

        if self.unitTest:
            self.printHeader('Using flask ' + self.flask_url)
            self.cl = client.HPLeftHandClient(self.flask_url)
            parsed_url = urlparse(self.flask_url)
            userArg = '-user=%s' % self.user
            passwordArg = '-password=%s' % self.password
            portArg = '-port=%s' % parsed_url.port

            script = 'HPLeftHandMockServer_flask.py'
            path = "%s/%s" % (cwd, script)
            try:
                if self.startFlask:
                    self.mockServer = subprocess.Popen([sys.executable,
                                                        path,
                                                        userArg,
                                                        passwordArg,
                                                        portArg],
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       stdin=subprocess.PIPE)
                else:
                    pass
            except Exception:
                pass
            time.sleep(1)
        else:
            self.printHeader('Using LeftHand ' + self.url_lhos)
            self.cl = client.HPLeftHandClient(self.url_lhos)

        if self.debug:
            self.cl.debug_rest(True)

        self.cl.login(self.user, self.password)

    def tearDown(self):
        self.cl.logout()
        if self.unitTest and self.startFlask:
            #TODO: it seems to kill all the process except the last one...
            #don't know why
            self.mockServer.kill()

    def printHeader(self, name):
        print("\n##Start testing '%s'" % name)

    def printFooter(self, name):
        print("##Compeleted testing '%s\n" % name)

    def findInDict(self, dic, key, value=None):
        for i in dic:
            if key in i:
                if value:
                    if i[key] == value:
                        return True
                else:  # If value is None, only check key
                    return True

        return False
