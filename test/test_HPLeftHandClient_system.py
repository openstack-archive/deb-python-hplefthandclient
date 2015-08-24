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

"""Test class of LeftHand Client system level APIs """

import test_HPLeftHandClient_base


class HPLeftHandClientSystemTestCase(test_HPLeftHandClient_base.
                                     HPLeftHandClientBaseTestCase):

    def setUp(self):
        super(HPLeftHandClientSystemTestCase, self).setUp()

    def tearDown(self):
        super(HPLeftHandClientSystemTestCase, self).tearDown()

    def test_1_get_api_version(self):
        self.printHeader('get_api_version')
        version = self.cl.getApiVersion()
        self.assertTrue(version is not None)
        self.printFooter('get_api_version')
