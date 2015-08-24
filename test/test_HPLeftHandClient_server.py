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

"""Test class of LeftHand Client handling servers """

import test_HPLeftHandClient_base

from hplefthandclient import exceptions

VOLUME_NAME1 = 'VOLUME1_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
VOLUME_NAME2 = 'VOLUME2_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
VOLUME_NAME3 = 'VOLUME3_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
SERVER_NAME1 = 'SERVER1_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
SERVER_NAME2 = 'SERVER2_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
IQN1 = 'iqn.1993-08.org.debian:01:00000' + test_HPLeftHandClient_base.TIME
IQN2 = 'iqn.1993-08.org.debian:01:00001' + test_HPLeftHandClient_base.TIME


class HPLeftHandClientServerTestCase(test_HPLeftHandClient_base.
                                     HPLeftHandClientBaseTestCase):

    def setUp(self):
        super(HPLeftHandClientServerTestCase, self).setUp()

        try:
            cluster_info = self.cl.getClusterByName(
                test_HPLeftHandClient_base.
                HPLeftHandClientBaseTestCase.cluster)
            self.cluster_id = cluster_info['id']
        except Exception:
            pass

    def tearDown(self):

        try:
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.cl.deleteVolume(volume_info['id'])
        except Exception:
            pass
        try:
            volume_info = self.cl.getVolumeByName(VOLUME_NAME2)
            self.cl.deleteVolume(volume_info['id'])
        except Exception:
            pass
        try:
            volume_info = self.cl.getVolumeByName(VOLUME_NAME3)
            self.cl.deleteVolume(volume_info['id'])
        except Exception:
            pass
        try:
            server_info = self.cl.getServerByName(SERVER_NAME1)
            self.cl.deleteServer(server_info['id'])
        except Exception:
            pass
        try:
            server_info = self.cl.getServerByName(SERVER_NAME2)
            self.cl.deleteServer(server_info['id'])
        except Exception:
            pass

        super(HPLeftHandClientServerTestCase, self).tearDown()

    def test_1_create_server(self):
        self.printHeader('create_server')

        optional = {'description': "some comment"}
        self.cl.createServer(SERVER_NAME1, IQN1, optional=optional)

        self.printFooter('create_server')

    def test_1_create_server_duplicate_name(self):
        self.printHeader('create_server_duplicate_name')

        optional = {'description': "some comment"}
        self.cl.createServer(SERVER_NAME1, IQN1, optional=optional)
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.createServer,
            SERVER_NAME1,
            IQN1,
            optional=optional)

        self.printFooter('create_server_duplicate_name')

    def test_1_create_server_missing_name(self):
        self.printHeader('create_server_missing_name')

        optional = {'description': "some comment"}
        self.assertRaises(
            exceptions.HTTPBadRequest,
            self.cl.createServer,
            None,
            IQN1,
            optional=optional)

        self.printFooter('create_server_missing_name')

    def test_2_add_server_access(self):
        self.printHeader('add_server_access')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.cl.addServerAccess(volume_info['id'],
                                server_info['id'],
                                optional={'lun': 0})

        # verify access was added
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_name = volume_info['volumeACL'][0]['server']['name']
        self.assertEqual(SERVER_NAME1, server_name)

        self.printFooter('add_server_access')

    def test_2_add_server_access_already_exists(self):
        self.printHeader('add_server_access_already_exists')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.cl.addServerAccess(volume_info['id'], server_info['id'])
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.addServerAccess,
            volume_info['id'],
            server_info['id']
        )

        self.printFooter('add_server_access_already_exists')

    def test_2_add_server_access_missing_volume(self):
        self.printHeader('add_server_access_missing_volume')

        self.cl.createServer(SERVER_NAME1, IQN1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.addServerAccess,
            self.MISSING_VOLUME_ID,
            server_info['id'])

        self.printFooter('add_server_access_missing_volume')

    def test_2_add_server_access_missing_server(self):
        self.printHeader('add_server_access_missing_server')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.addServerAccess,
            volume_info['id'],
            self.MISSING_SERVER_ID)

        self.printFooter('add_server_access_missing_server')

    def test_2_remove_server_access(self):
        self.printHeader('remove_server_access')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.cl.addServerAccess(volume_info['id'],
                                server_info['id'],
                                optional={'lun': 0})
        self.cl.removeServerAccess(volume_info['id'], server_info['id'])

        # verify access was removed
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        print(volume_info)
        self.assertIsNone(volume_info['volumeACL'])

        self.printFooter('remove_server_access')

    def test_2_remove_server_access_access_not_set(self):
        self.printHeader('remove_server_access_access_not_set')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.cl.removeServerAccess(volume_info['id'], server_info['id'])

        # No exception expected in this case

        self.printFooter('remove_server_access_access_not_set')

    def test_2_remove_server_access_missing_volume(self):
        self.printHeader('remove_server_access_missing_volume')

        self.cl.createServer(SERVER_NAME1, IQN1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.removeServerAccess,
            self.MISSING_VOLUME_ID,
            server_info['id'])

        self.printFooter('remove_server_access_missing_volume')

    def test_2_remove_server_access_missing_server(self):
        self.printHeader('remove_server_access_missing_server')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        self.assertRaises(
            exceptions.HTTPServerError,
            self.cl.removeServerAccess,
            volume_info['id'],
            self.MISSING_SERVER_ID)

        self.printFooter('remove_server_access_missing_server')

    def test_3_find_server_volumes(self):
        self.printHeader('find_server_volumes')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}

        # Create first volume and a server
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        result = self.cl.findServerVolumes(SERVER_NAME1)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 0)

        # Add access to first volume
        self.cl.addServerAccess(volume_info['id'], server_info['id'])
        result = self.cl.findServerVolumes(SERVER_NAME1)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 1)
        self.assertIn(VOLUME_NAME1, volume_list)

        # Create second volume
        self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        volume_info2 = self.cl.getVolumeByName(VOLUME_NAME2)
        result = self.cl.findServerVolumes(SERVER_NAME1)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 1)
        self.assertNotIn(VOLUME_NAME2, volume_list)

        # Add access to second volume
        self.cl.addServerAccess(volume_info2['id'], server_info['id'])
        result = self.cl.findServerVolumes(SERVER_NAME1)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 2)
        self.assertIn(VOLUME_NAME1, volume_list)
        self.assertIn(VOLUME_NAME2, volume_list)

        # Create third volume and a new server, add access
        self.cl.createVolume(VOLUME_NAME3, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME2, IQN2)
        volume_info3 = self.cl.getVolumeByName(VOLUME_NAME3)
        server_info2 = self.cl.getServerByName(SERVER_NAME2)
        self.cl.addServerAccess(volume_info3['id'], server_info2['id'])
        result = self.cl.findServerVolumes(SERVER_NAME2)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 1)
        self.assertIn(VOLUME_NAME3, volume_list)
        result = self.cl.findServerVolumes(SERVER_NAME1)
        volume_list = [vol['name'] for vol in result]
        self.assertEqual(len(volume_list), 2)
        self.assertNotIn(VOLUME_NAME3, volume_list)

        self.printFooter('find_server_volumes')

    def test_3_find_server_volumes_empty(self):
        self.printHeader('find_server_volumes_empty')

        expected = []
        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                             self.GB_TO_BYTES, optional)
        self.cl.createServer(SERVER_NAME1, IQN1)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        server_info = self.cl.getServerByName(SERVER_NAME1)
        self.cl.addServerAccess(volume_info['id'], server_info['id'])
        volume_info = self.cl.getVolumeByName(VOLUME_NAME2)
        self.cl.addServerAccess(volume_info['id'], server_info['id'])
        result = self.cl.findServerVolumes('bogus_server')
        self.assertEqual(expected, result)

        self.printFooter('find_server_volumes_empty')

    def test_4_get_servers(self):
        self.printHeader('get_servers')

        self.cl.createServer(SERVER_NAME1, IQN1)
        result = self.cl.getServers()
        self.assertTrue(self.findInDict(result['members'],
                                        'name',
                                        SERVER_NAME1))

        self.printFooter('get_servers')

    def test_4_get_server_by_name(self):
        self.printHeader('get_server_by_name')

        self.cl.createServer(SERVER_NAME1, IQN1)
        result = self.cl.getServerByName(SERVER_NAME1)
        self.assertEqual(SERVER_NAME1, result['name'])

        self.printFooter('get_server_by_name')

    def test_4_get_server_by_name_missing_server(self):
        self.printHeader('get_server_by_name_missing_server')

        self.assertRaises(
            exceptions.HTTPNotFound,
            self.cl.getServerByName,
            'missing_server')

        self.printFooter('get_server_by_name_missing_server')
