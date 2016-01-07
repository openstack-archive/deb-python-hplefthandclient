# (c) Copyright 2015-2016 Hewlett Packard Enterprise Development LP
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

import time
import unittest
from testconfig import config

import test_HPELeftHandClient_base

from hpelefthandclient import exceptions

VOLUME_NAME1 = 'VOLUME1_UNIT_TEST_' + test_HPELeftHandClient_base.TIME
VOLUME_NAME2 = 'VOLUME2_UNIT_TEST_' + test_HPELeftHandClient_base.TIME
VOLUME_NAME3 = 'VOLUME3_UNIT_TEST_' + test_HPELeftHandClient_base.TIME
SNAP_NAME1 = 'SNAP_UNIT_TEST1_' + test_HPELeftHandClient_base.TIME
SNAP_NAME2 = 'SNAP_UNIT_TEST2_' + test_HPELeftHandClient_base.TIME
SKIP_FLASK_RCOPY_MESSAGE = ("Remote copy is not configured to be tested "
                            "on live arrays.")
REMOTE_SNAP_SCHED_NAME = 'VOLUME1_SCHED' + test_HPELeftHandClient_base.TIME
REMOTE_SNAP_RECUR_PERIOD = '1800'
REMOTE_SNAP_START_TIME = '1970-01-01T00:00:00Z'
REMOTE_SNAP_RETENTION_COUNT = '10'
REMOTE_SNAP_REMOTE_RETENTION_COUNT = '10'


def is_live_test():
    return config['TEST']['unit'].lower() == 'false'


# NOTE(aorourke): Remote copy related tests will be skipped if:
#    1). They are being run against the flask server -or-
#    2). run_remote_copy is set to false in config.ini, which it is by default
# If you are making any changes that may touch anything remote copy related,
# config.ini needs to be properly modified in order to run these tests
# against live arrays. The results must be verified to ensure they are still
# passing as expected.
def no_remote_copy():
    unit_test = config['TEST']['unit'].lower() == 'false'
    remote_copy = config['TEST']['run_remote_copy'].lower() == 'true'
    run_remote_copy = not remote_copy or not unit_test
    return run_remote_copy


class HPELeftHandClientVolumeTestCase(test_HPELeftHandClient_base.
                                      HPELeftHandClientBaseTestCase):

    # Minimum API version needed for consistency group support
    MIN_CG_API_VERSION = '1.2'

    def setUp(self):
        ssh = False
        if is_live_test():
            ssh = True
        super(HPELeftHandClientVolumeTestCase, self).setUp(withSSH=ssh)

        try:
            cluster_info = self.cl.getClusterByName(
                test_HPELeftHandClient_base.
                HPELeftHandClientBaseTestCase.cluster)
            self.cluster_id = cluster_info['id']
            self.cluster_name = cluster_info['name']
            self.ip_addresses = cluster_info['storageModuleIPAddresses']
        except Exception:
            self.cluster_id = 21
            self.cluster_name = 'ClusterVSA309'
            self.ip_addresses = ['10.10.30.165']
            pass

        try:
            # Get secondary cluster information if needed.
            if self.secondary_cl:
                sec_cluster_info = self.secondary_cl.getClusterByName(
                    test_HPELeftHandClient_base.
                    HPELeftHandClientBaseTestCase.secondary_cluster)
                self.sec_cluster_id = sec_cluster_info['id']
                self.sec_cluster_name = sec_cluster_info['name']
                self.sec_ip_addresses = (
                    sec_cluster_info['storageModuleIPAddresses'])
        except Exception:
            pass

    def tearDown(self):

        try:
            self.deleteRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
        except Exception:
            pass
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
            self.secondary_cl.deleteRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Rmt")
        except Exception:
            pass
        try:
            volume_info = self.secondary_cl.getVolumeByName(VOLUME_NAME1)
            self.secondary_cl.deleteVolume(volume_info['id'])
        except Exception:
            pass

        super(HPELeftHandClientVolumeTestCase, self).tearDown()

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
            test_HPELeftHandClient_base.HPELeftHandClientBaseTestCase.cluster,
            fields=['members[id]', 'members[uri]', 'members[clusterName]'])

        self.assertTrue(self.findInDict(vols['members'], 'id'))
        self.assertTrue(self.findInDict(vols['members'], 'uri'))
        self.assertTrue(self.findInDict(vols['members'], 'clusterName'))
        self.assertFalse(self.findInDict(vols['members'], 'name'))

        vols = self.cl.getVolumes(
            test_HPELeftHandClient_base.HPELeftHandClientBaseTestCase.cluster,
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

    def test_6_modify_snapshot(self):
        self.printHeader('modify_snapshot')
        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        option = {'inheritAccess': True}
        self.cl.createSnapshot(SNAP_NAME2, volume_info['id'], option)

        new_options = {'description': 'test snapshot'}
        snap_info = self.cl.getSnapshotByName(SNAP_NAME2)
        self.cl.modifySnapshot(snap_info['id'], new_options)
        new_snap_info = self.cl.getSnapshotByName(SNAP_NAME2)
        self.assertIn('description', new_snap_info)
        self.assertEqual(new_options['description'],
                         new_snap_info['description'])
        self.cl.deleteSnapshot(snap_info['id'])

        self.printFooter('modify_snapshot')

    def test_6_modify_snapshot_nonExistSnapshot(self):
        self.printHeader('modify_snapshot_nonExistSnapshot')

        fake_snap_id = 12345
        new_options = {'description': 'test snapshot'}
        self.assertRaises(exceptions.HTTPServerError,
                          self.cl.modifySnapshot,
                          fake_snap_id,
                          new_options)

        self.printFooter('modify_snapshot_nonExistSnapshot')

    @unittest.skipIf(not is_live_test(), "Only runs on live array.")
    def test_6_get_snapshot_parent_volume(self):
        self.printHeader('get_snapshot_parent_volume')

        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        option = {'inheritAccess': True}
        self.cl.createSnapshot(SNAP_NAME1, volume_info['id'], option)

        parent_vol = self.cl.getSnapshotParentVolume(SNAP_NAME1)

        self.assertEqual(VOLUME_NAME1, parent_vol['name'])

        self.printFooter('get_snapshot_parent_volume')

    @unittest.skipIf(not is_live_test(), "Only runs on live array.")
    def test_6_get_snapshot_parent_volume_snapshot_invalid(self):
        self.printHeader('get_snapshot_parent_volume_snapshot_invalid')

        self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                             self.GB_TO_BYTES)
        volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
        option = {'inheritAccess': True}
        self.cl.createSnapshot(SNAP_NAME1, volume_info['id'], option)

        self.assertRaises(exceptions.HTTPNotFound,
                          self.cl.getSnapshotParentVolume,
                          "fake_snap")

        self.printFooter('get_snapshot_parent_volume_snapshot_invalid')

    def test_7_get_ip_from_cluster(self):
        self.printHeader('get_ip_from_cluster')

        try:
            expected_ip = self.ip_addresses[0]
            target_ip = self.cl.getIPFromCluster(self.cluster_name)
            self.assertEqual(expected_ip, target_ip)
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('get_ip_from_cluster')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_8_make_volume_remote(self):
        self.printHeader('make_volume_remote')

        try:
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertEqual(True, volume_info['isPrimary'])

            self.cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)
            time.sleep(3)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertEqual(False, volume_info['isPrimary'])

            snap_info = self.cl.getSnapshotByName(SNAP_NAME1)
            self.assertEqual(True, snap_info['isPrimary'])
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('make_volume_remote')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_8_make_volume_primary(self):
        self.printHeader('make_volume_primary')

        try:
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertEqual(True, volume_info['isPrimary'])

            # Make volume remote
            self.cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)
            time.sleep(3)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertEqual(False, volume_info['isPrimary'])

            # Make volume primary
            self.cl.makeVolumePrimary(VOLUME_NAME1)
            time.sleep(3)
            volume_info = self.cl.getVolumeByName(VOLUME_NAME1)
            self.assertEqual(True, volume_info['isPrimary'])
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('make_volume_primary')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_9_create_remote_snapshot_schedule(self):
        self.printHeader('create_remote_snapshot_schedule')

        try:
            # Create primary volume
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)

            # Create secondary volume on target array
            self.secondary_cl.createVolume(VOLUME_NAME1, self.sec_cluster_id,
                                           self.GB_TO_BYTES)

            # Make secondary volume a remote volume
            self.secondary_cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)

            # Create the remote snapshot schedule
            target_ip = self.secondary_cl.getIPFromCluster(
                self.secondary_cluster)
            success = self.cl.createRemoteSnapshotSchedule(
                VOLUME_NAME1,
                REMOTE_SNAP_SCHED_NAME,
                REMOTE_SNAP_RECUR_PERIOD,
                REMOTE_SNAP_START_TIME,
                REMOTE_SNAP_RETENTION_COUNT,
                self.secondary_cluster,
                REMOTE_SNAP_REMOTE_RETENTION_COUNT,
                VOLUME_NAME1,
                target_ip,
                self.secondary_user,
                self.secondary_password)
            self.assertEqual(True, success)

            # Check to be sure the schedule exists
            does_schedule_exist = self.cl.doesRemoteSnapshotScheduleExist(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            self.assertEqual(True, does_schedule_exist)
            does_remote_schedule_exist = (
                self.secondary_cl.doesRemoteSnapshotScheduleExist(
                    REMOTE_SNAP_SCHED_NAME + "_Rmt"))
            self.assertEqual(True, does_remote_schedule_exist)

            # Get schedule and check values
            schedule = self.cl.getRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            schedule_string = ''.join(schedule)
            self.assertRegexpMatches(
                schedule_string, ".*volumeName\s+" + VOLUME_NAME1)
            self.assertRegexpMatches(
                schedule_string, ".*name\s+" + REMOTE_SNAP_SCHED_NAME)
            self.assertRegexpMatches(
                schedule_string, ".*period\s+" + REMOTE_SNAP_RECUR_PERIOD)
            self.assertRegexpMatches(
                schedule_string, ".*startTime\s+" + REMOTE_SNAP_START_TIME)
            self.assertRegexpMatches(
                schedule_string, ".*retentionCount\s+10")
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('create_remote_snapshot_schedule')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_9_delete_remote_snapshot_schedule(self):
        self.printHeader('delete_remote_snapshot_schedule')

        try:
            # Create primary volume
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)

            # Create secondary volume on target array
            self.secondary_cl.createVolume(VOLUME_NAME1, self.sec_cluster_id,
                                           self.GB_TO_BYTES)

            # Make secondary volume a remote volume
            self.secondary_cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)

            # Create the remote snapshot schedule
            target_ip = self.secondary_cl.getIPFromCluster(
                self.secondary_cluster)
            success = self.cl.createRemoteSnapshotSchedule(
                VOLUME_NAME1,
                REMOTE_SNAP_SCHED_NAME,
                REMOTE_SNAP_RECUR_PERIOD,
                REMOTE_SNAP_START_TIME,
                REMOTE_SNAP_RETENTION_COUNT,
                self.secondary_cluster,
                REMOTE_SNAP_REMOTE_RETENTION_COUNT,
                VOLUME_NAME1,
                target_ip,
                self.secondary_user,
                self.secondary_password)
            self.assertEqual(True, success)

            # Check to be sure the schedule exists
            does_schedule_exist = self.cl.doesRemoteSnapshotScheduleExist(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            self.assertEqual(True, does_schedule_exist)
            does_remote_schedule_exist = (
                self.secondary_cl.doesRemoteSnapshotScheduleExist(
                    REMOTE_SNAP_SCHED_NAME + "_Rmt"))
            self.assertEqual(True, does_remote_schedule_exist)

            # Delete the remote snapshot schedule
            success = self.cl.deleteRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            self.assertEqual(True, success)

            # Check to be sure the schedule no longer exists
            self.assertRaises(
                exceptions.SSHException,
                self.cl.doesRemoteSnapshotScheduleExist,
                REMOTE_SNAP_SCHED_NAME + "_Pri")
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('delete_remote_snapshot_schedule')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_10_stop_remote_snapshot_schedule(self):
        self.printHeader('stop_remote_snapshot_schedule')

        try:
            # Create primary volume
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)

            # Create secondary volume on target array
            self.secondary_cl.createVolume(VOLUME_NAME1, self.sec_cluster_id,
                                           self.GB_TO_BYTES)

            # Make secondary volume a remote volume
            self.secondary_cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)

            # Create the remote snapshot schedule
            target_ip = self.secondary_cl.getIPFromCluster(
                self.secondary_cluster)
            success = self.cl.createRemoteSnapshotSchedule(
                VOLUME_NAME1,
                REMOTE_SNAP_SCHED_NAME,
                REMOTE_SNAP_RECUR_PERIOD,
                REMOTE_SNAP_START_TIME,
                REMOTE_SNAP_RETENTION_COUNT,
                self.secondary_cluster,
                REMOTE_SNAP_REMOTE_RETENTION_COUNT,
                VOLUME_NAME1,
                target_ip,
                self.secondary_user,
                self.secondary_password)
            self.assertEqual(True, success)

            # Check to be sure the schedule exists
            does_schedule_exist = self.cl.doesRemoteSnapshotScheduleExist(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            self.assertEqual(True, does_schedule_exist)
            does_remote_schedule_exist = (
                self.secondary_cl.doesRemoteSnapshotScheduleExist(
                    REMOTE_SNAP_SCHED_NAME + "_Rmt"))
            self.assertEqual(True, does_remote_schedule_exist)

            # Stop the remote snapshot schedule. LH needs time to create and
            # start the schedule.
            time.sleep(5)
            self.cl.stopRemoteSnapshotSchedule(REMOTE_SNAP_SCHED_NAME + "_Pri")

            # Get schedule and check it has stopped
            schedule = self.cl.getRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            schedule_string = ''.join(schedule)
            self.assertRegexpMatches(
                schedule_string, ".*paused\s+true")
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('stop_remote_snapshot_schedule')

    @unittest.skipIf(no_remote_copy(), SKIP_FLASK_RCOPY_MESSAGE)
    def test_10_start_remote_snapshot_schedule(self):
        self.printHeader('start_remote_snapshot_schedule')

        try:
            # Create primary volume
            self.cl.createVolume(VOLUME_NAME1, self.cluster_id,
                                 self.GB_TO_BYTES)

            # Create secondary volume on target array
            self.secondary_cl.createVolume(VOLUME_NAME1, self.sec_cluster_id,
                                           self.GB_TO_BYTES)

            # Make secondary volume a remote volume
            self.secondary_cl.makeVolumeRemote(VOLUME_NAME1, SNAP_NAME1)

            # Create the remote snapshot schedule
            target_ip = self.secondary_cl.getIPFromCluster(
                self.secondary_cluster)
            success = self.cl.createRemoteSnapshotSchedule(
                VOLUME_NAME1,
                REMOTE_SNAP_SCHED_NAME,
                REMOTE_SNAP_RECUR_PERIOD,
                REMOTE_SNAP_START_TIME,
                REMOTE_SNAP_RETENTION_COUNT,
                self.secondary_cluster,
                REMOTE_SNAP_REMOTE_RETENTION_COUNT,
                VOLUME_NAME1,
                target_ip,
                self.secondary_user,
                self.secondary_password)
            self.assertEqual(True, success)

            # Check to be sure the schedule exists
            does_schedule_exist = self.cl.doesRemoteSnapshotScheduleExist(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            self.assertEqual(True, does_schedule_exist)
            does_remote_schedule_exist = (
                self.secondary_cl.doesRemoteSnapshotScheduleExist(
                    REMOTE_SNAP_SCHED_NAME + "_Rmt"))
            self.assertEqual(True, does_remote_schedule_exist)

            # Stop the remote snapshot schedule. LH needs time to create and
            # start the schedule.
            time.sleep(5)
            self.cl.stopRemoteSnapshotSchedule(REMOTE_SNAP_SCHED_NAME + "_Pri")

            # Get schedule and check it has stopped
            schedule = self.cl.getRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            schedule_string = ''.join(schedule)
            self.assertRegexpMatches(
                schedule_string, ".*paused\s+true")

            # Start the remote snapshot schedule
            self.cl.startRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")

            # Get schedule and check it has started
            schedule = self.cl.getRemoteSnapshotSchedule(
                REMOTE_SNAP_SCHED_NAME + "_Pri")
            schedule_string = ''.join(schedule)
            self.assertRegexpMatches(
                schedule_string, ".*paused\s+false")
        except Exception as ex:
            print(ex)
            self.fail("Failed with unexpected exception")
        self.printFooter('start_remote_snapshot_schedule')
#testing
#suite = unittest.TestLoader().loadTestsFromTestCase(
#    HPELeftHandClientVolumeTestCase)
#unittest.TextTestRunner(verbosity=2).run(suite)
