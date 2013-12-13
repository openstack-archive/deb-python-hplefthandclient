# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright 2009-2012 10gen, Inc.
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
sys.path.insert(0, os.path.realpath(os.path.abspath('../')))

from hplefthandclient import client
import unittest
import subprocess
import time
import inspect
from testconfig import config
from urlparse import urlparse

# pip install nose-testconfig

# e.g.
# nosetests test_HPLeftHandClient_volume.py -v --tc-file config.ini


class HPLeftHandClientBaseTestCase(unittest.TestCase):

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

            script = 'test_HPLeftHandMockServer_flask.py'
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
        print "\n##Start testing '%s'" % name

    def printFooter(self, name):
        print "##Compeleted testing '%s\n" % name

    def findInDict(self, dic, key, value):
        for i in dic:
            if key in i and i[key] == value:
                return True
