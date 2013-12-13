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

"""Test class of LeftHand Client handling volumes & snapshots """

import sys
import os
sys.path.insert(0, os.path.realpath(os.path.abspath('../')))

from hplefthandclient import exceptions
import test_HPLeftHandClient_base

VOLUME_NAME1 = 'VOLUME1_UNIT_TEST'
VOLUME_NAME2 = 'VOLUME2_UNIT_TEST'
VOLUME_NAME3 = 'VOLUME3_UNIT_TEST'
SNAP_NAME1 = 'SNAP_UNIT_TEST'


class HPLeftHandClientVolumeTestCase(test_HPLeftHandClient_base.
                                     HPLeftHandClientBaseTestCase):

    cluster_id = 0
    GB_TO_BYTES = 1073741824

    def setUp(self):
        super(HPLeftHandClientVolumeTestCase, self).setUp()

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
        except Exception as ex:
            print ex
            pass
        try:
            volume_info = self.cl.getVolumeByName(VOLUME_NAME2)
            self.cl.deleteVolume(volume_info['id'])
        except Exception as ex:
            print ex
            pass

        super(HPLeftHandClientVolumeTestCase, self).tearDown()

    def test_1_create_volume(self):
        self.printHeader('create_volume')

        try:
            #add one
            optional = {'description': 'test volume',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 1 * self.GB_TO_BYTES, optional)
        except Exception as ex:
            print ex
            self.fail('Failed to create volume')
            return

        try:
            #check
            vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertIsNotNone(vol1)
            volName = vol1['name']
            self.assertEqual(VOLUME_NAME1, volName)

        except Exception as ex:
            print ex
            self.fail('Failed to get volume')
            return

        try:
            #add another
            optional = {'description': 'test volume2',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                                 1 * self.GB_TO_BYTES, optional)
        except Exception as ex:
            print ex
            self.fail('Failed to create volume')
            return

        try:
            #check
            vol2 = self.cl.getVolumeByName(VOLUME_NAME2)
            self.assertIsNotNone(vol2)
            volName = vol2['name']
            self.assertEqual(VOLUME_NAME2, volName)
        except Exception as ex:
            print ex
            self.fail("Failed to get volume")

        self.printFooter('create_volume')

    def test_1_create_volume_duplicate_name(self):
        self.printHeader('create_volume_duplicate_name')

        #add one and check
        try:
            optional = {'description': 'test volume',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 2 * self.GB_TO_BYTES, optional)
        except Exception as ex:
            print ex
            self.fail("Failed to create volume")

        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.createVolume,
                          VOLUME_NAME1,
                          self.cluster_id,
                          2 * self.GB_TO_BYTES,
                          optional)
        self.printFooter('create_volume_duplicate_name')

    def test_1_create_volume_tooLarge(self):
        self.printHeader('create_volume_tooLarge')
        optional = {'description': 'test volume',
                    'isThinProvisioned': False}

        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.createVolume,
                          VOLUME_NAME1,
                          self.cluster_id,
                          16777218 * self.GB_TO_BYTES,
                          optional)

        self.printFooter('create_volume_tooLarge')

    def test_2_get_volume_bad(self):
        self.printHeader('get_volume_bad')

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeByName,
                          'NoSuchVolume')

        self.printFooter('get_volume_bad')

    def test_2_get_volumes(self):
        self.printHeader('get_volumes')

        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             3 * self.GB_TO_BYTES)
        self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                             3 * self.GB_TO_BYTES)

        vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
        vol2 = self.cl.getVolumeByName(VOLUME_NAME2)

        vols = self.cl.getVolumes()

        self.assertTrue(self.findInDict(vols['members'], 'name', vol1['name']))
        self.assertTrue(self.findInDict(vols['members'], 'name', vol2['name']))

        self.printFooter('get_volumes')

    def test_3_delete_volume_nonExist(self):
        self.printHeader('delete_volume_nonExist')
        volume_id = -1

        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.deleteVolume,
                          volume_id)
        self.printFooter('delete_volume_nonExist')

    def test_3_delete_volumes(self):
        self.printHeader('delete_volumes')

        try:
            optional = {'description': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 1 * self.GB_TO_BYTES, optional)
            vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
            self.printHeader('vol1 id %s' % vol1['id'])
            self.printHeader('members %s' % vol1)
        except Exception as ex:
            print ex
            self.fail('Failed to create volume %s' % VOLUME_NAME1)

        try:
            optional = {'description': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                                 1 * self.GB_TO_BYTES, optional)
            vol2 = self.cl.getVolumeByName(VOLUME_NAME2)
            self.printHeader('vol2 id %s' % vol2['id'])
        except Exception as ex:
            print ex
            self.fail('Failed to create volume %s' % VOLUME_NAME2)

        try:
            self.cl.deleteVolume(vol1['id'])
        except Exception as ex:
            print ex
            self.fail('Failed to delete %s' % vol1['id'])

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeByName,
                          VOLUME_NAME1)

        try:
            self.cl.deleteVolume(vol2['id'])
        except Exception as ex:
            print ex
            self.fail('Failed to delete %s' % vol2['id'])

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeByName,
                          VOLUME_NAME2)
        self.printFooter('delete_volumes')

    def test_4_create_snapshot(self):
        self.printHeader('create_snapshot')

        try:
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 1 * self.GB_TO_BYTES)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            option = {'inheritAccess': True}
            self.cl.createSnapshot(SNAP_NAME1, volume_info['id'], option)
        except Exception as ex:
            print ex
            self.fail("Failed with unexpected exception")

        snap_info = self.cl.getSnapshotByName(SNAP_NAME1)
        self.cl.deleteSnapshot(snap_info['id'])
        self.printFooter('create_snapshot')

    def test_4_create_snapshot_nonExistVolume(self):
        self.printHeader('create_snapshot_nonExistVolume')

        optional = {'description': 'test snapshot'}
        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.createSnapshot,
                          'UnitTestSnapshot',
                          -1,
                          optional)
        self.printFooter('create_snapshot_nonExistVolume')
#testing
#suite = unittest.TestLoader().loadTestsFromTestCase(HPLeftHandClientVolumeTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)
