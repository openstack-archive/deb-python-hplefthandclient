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

"""Test class of LeftHand Client handling volumes & snapshots """

import test_HPLeftHandClient_base

from hplefthandclient import exceptions

VOLUME_NAME1 = 'VOLUME1_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
VOLUME_NAME2 = 'VOLUME2_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
VOLUME_NAME3 = 'VOLUME3_UNIT_TEST_' + test_HPLeftHandClient_base.TIME
SNAP_NAME1 = 'SNAP_UNIT_TEST_' + test_HPLeftHandClient_base.TIME


class HPLeftHandClientVolumeTestCase(test_HPLeftHandClient_base.
                                     HPLeftHandClientBaseTestCase):

    # Minimum API version needed for consistency group support
    MIN_CG_API_VERSION = '1.2'

    def setUp(self):
        super(HPLeftHandClientVolumeTestCase, self).setUp()

        try:
            cluster_info = self.cl.getClusterByName(
                test_HPLeftHandClient_base.
                HPLeftHandClientBaseTestCase.cluster)
            self.cluster_id = cluster_info['id']
            self.cluster_name = cluster_info['name']
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

        super(HPLeftHandClientVolumeTestCase, self).tearDown()

    def test_1_create_volume(self):
        self.printHeader('create_volume')

        try:
            #add one
            optional = {'description': 'test volume',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            #check
            vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertIsNotNone(vol1)
            volName = vol1['name']
            self.assertEqual(VOLUME_NAME1, volName)

        except Exception as ex:
            print(ex)
            self.fail('Failed to get volume')
            return

        try:
            #add another
            optional = {'description': 'test volume2',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                                 self.GB_TO_BYTES, optional)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume')
            return

        try:
            #check
            vol2 = self.cl.getVolumeByName(VOLUME_NAME2)
            self.assertIsNotNone(vol2)
            volName = vol2['name']
            self.assertEqual(VOLUME_NAME2, volName)
        except Exception as ex:
            print(ex)
            self.fail("Failed to get volume")

        self.printFooter('create_volume')

    def test_1_create_volume_check_size(self):
        self.printHeader('create_volume_check_size')

        optional = {'description': 'test volume',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES, optional)

        optional = {'description': 'test volume 2',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                             2 * self.GB_TO_BYTES, optional)

        optional = {'description': 'test volume 3',
                    'isThinProvisioned': True}
        self.cl.createVolume(VOLUME_NAME3, self.cluster_id,
                             3 * self.GB_TO_BYTES, optional)

        vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
        vol2 = self.cl.getVolumeByName(VOLUME_NAME2)
        vol3 = self.cl.getVolumeByName(VOLUME_NAME3)

        self.assertEqual(self.GB_TO_BYTES, vol1['size'])
        self.assertEqual(2 * self.GB_TO_BYTES, vol2['size'])
        self.assertEqual(3 * self.GB_TO_BYTES, vol3['size'])

        self.printFooter('create_volume_check_size')

    def test_1_create_volume_duplicate_name(self):
        self.printHeader('create_volume_duplicate_name')

        #add one and check
        try:
            optional = {'description': 'test volume',
                        'isThinProvisioned': True}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES, optional)
        except Exception as ex:
            print(ex)
            self.fail("Failed to create volume")

        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.createVolume,
                          VOLUME_NAME1,
                          self.cluster_id,
                          self.GB_TO_BYTES,
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
                             self.GB_TO_BYTES)
        self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                             self.GB_TO_BYTES)

        vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
        vol2 = self.cl.getVolumeByName(VOLUME_NAME2)

        vols = self.cl.getVolumes()

        self.assertTrue(self.findInDict(vols['members'], 'name', vol1['name']))
        self.assertTrue(self.findInDict(vols['members'], 'name', vol2['name']))

        self.printFooter('get_volumes')

    def test_2_get_volumes_query(self):
        self.printHeader('get_volumes')

        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES)

        vols = self.cl.getVolumes(
            test_HPLeftHandClient_base.HPLeftHandClientBaseTestCase.cluster,
            fields=['members[id]', 'members[uri]', 'members[clusterName]'])

        self.assertTrue(self.findInDict(vols['members'], 'id'))
        self.assertTrue(self.findInDict(vols['members'], 'uri'))
        self.assertTrue(self.findInDict(vols['members'], 'clusterName'))
        self.assertFalse(self.findInDict(vols['members'], 'name'))

        vols = self.cl.getVolumes(
            test_HPLeftHandClient_base.HPLeftHandClientBaseTestCase.cluster,
            fields=None)

        self.printFooter('get_volumes')

    def test_3_delete_volume_nonExist(self):
        self.printHeader('delete_volume_nonExist')

        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.deleteVolume,
                          self.MISSING_VOLUME_ID)
        self.printFooter('delete_volume_nonExist')

    def test_3_delete_volumes(self):
        self.printHeader('delete_volumes')

        try:
            optional = {'description': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES, optional)
            vol1 = self.cl.getVolumeByName(VOLUME_NAME1)
            self.printHeader('vol1 id %s' % vol1['id'])
            self.printHeader('members %s' % vol1)
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume %s' % VOLUME_NAME1)

        try:
            optional = {'description': 'Made by flask.'}
            self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                                 self.GB_TO_BYTES, optional)
            vol2 = self.cl.getVolumeByName(VOLUME_NAME2)
            self.printHeader('vol2 id %s' % vol2['id'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to create volume %s' % VOLUME_NAME2)

        try:
            self.cl.deleteVolume(vol1['id'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete %s' % vol1['id'])

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeByName,
                          VOLUME_NAME1)

        try:
            self.cl.deleteVolume(vol2['id'])
        except Exception as ex:
            print(ex)
            self.fail('Failed to delete %s' % vol2['id'])

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getVolumeByName,
                          VOLUME_NAME2)
        self.printFooter('delete_volumes')

    def test_4_create_snapshot(self):
        self.printHeader('create_snapshot')

        try:
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            option = {'inheritAccess': True}
            self.cl.createSnapshot(SNAP_NAME1, volume_info['id'], option)
        except Exception as ex:
            print(ex)
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
                          self.MISSING_VOLUME_ID,
                          optional)
        self.printFooter('create_snapshot_nonExistVolume')

    def test_4_delete_snapshot_clonePoint(self):
        self.printHeader('delete_snapshot_clonePoint')

        # create volume
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)

        # snapshot the volume
        option = {'inheritAccess': True}
        self.cl.createSnapshot(SNAP_NAME1, volume_info['id'], option)

        # create volume from snapshot to create 'clone point'
        snap_info = self.cl.getSnapshotByName(SNAP_NAME1)
        self.cl.cloneSnapshot(VOLUME_NAME2, snap_info['id'])

        # try and delete snapshot clone point, assert error description
        # is the error we expect
        try:
            self.cl.deleteSnapshot(snap_info['id'])
        except exceptions.HTTPServerError as ex:
            in_use_msg = 'cannot be deleted because it is a clone point'
            assert in_use_msg in ex.get_description()
        self.printFooter('delete_snapshot_clonePoint')

    def test_5_create_snapshot_set(self):
        self.printHeader('create_snapshot_set')

        # dont run this test unless the API version is 1.2 or greater
        api_version = self.cl.getApiVersion()
        if api_version < self.MIN_CG_API_VERSION:
            ex_msg = ('Invalid LeftHand API version found (%(found)s).'
                      'Version %(minimum)s or greater required.'
                      'Aborting test.') % {'found': api_version,
                                           'minimum': self.MIN_CG_API_VERSION}
            print(ex_msg)
            self.printFooter('create_snapshot_set')
            return

        try:
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)
            self.cl.createVolume(VOLUME_NAME2, self.cluster_id,
                                 self.GB_TO_BYTES)
            volume1_info = self.cl.getVolumeByName(VOLUME_NAME1)
            volume2_info = self.cl.getVolumeByName(VOLUME_NAME2)
            option = {'inheritAccess': True}
            snap_set = [
                {"volumeName": VOLUME_NAME1, "volumeId": volume1_info['id'],
                 "snapshotName": SNAP_NAME1 + "-0"},
                {"volumeName": VOLUME_NAME2, "volumeId": volume2_info['id'],
                 "snapshotName": SNAP_NAME1 + "-1"}
            ]
            self.cl.createSnapshotSet(volume1_info['id'], snap_set, option)
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")

        snap1_info = self.cl.getSnapshotByName(SNAP_NAME1 + "-0")
        self.cl.deleteSnapshot(snap1_info['id'])
        snap2_info = self.cl.getSnapshotByName(SNAP_NAME1 + "-1")
        self.cl.deleteSnapshot(snap2_info['id'])
        self.printFooter('create_snapshot_set')

    def test_5_create_snapshot_set_nonExistVolume(self):
        self.printHeader('create_snapshot_set_nonExistVolume')

        # dont run this test unless the API version is 1.2 or greater
        api_version = self.cl.getApiVersion()
        if api_version < self.MIN_CG_API_VERSION:
            ex_msg = ('Invalid LeftHand API version found (%(found)s).'
                      'Version %(minimum)s or greater required.'
                      'Aborting test.') % {'found': api_version,
                                           'minimum': self.MIN_CG_API_VERSION}
            print(ex_msg)
            self.printFooter('create_snapshot_set_nonExistVolume')
            return

        optional = {'description': 'test snapshot set'}
        snap_set = [
            {"volumeName": "", "volumeId": 0,
             "snapshotName": "invalid"}
        ]
        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.createSnapshotSet,
                          self.MISSING_VOLUME_ID,
                          snap_set,
                          optional)
        self.printFooter('create_snapshot_set_nonExistVolume')
#testing
#suite = unittest.TestLoader().loadTestsFromTestCase(
#    HPLeftHandClientVolumeTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)
