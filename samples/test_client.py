import argparse
from os import sys
import os
import pprint

# this is a hack to get the hp driver module
# and it's utils module on the search path.
cmd_folder = os.path.realpath(os.path.abspath(".."))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from hplefthandclient import client, exceptions

parser = argparse.ArgumentParser()
parser.add_argument("-debug", help="Turn on http debugging", default=False,
                    action="store_true")
args = parser.parse_args()


cl = client.HPLeftHandClient("http://10.10.22.7:8080/lhos")
# This is the local flask server url
#cl = client.HPLeftHandClient("http://127.0.0.1:5000/lhos")
if "debug" in args and args.debug == True:
    cl.debug_rest(True)


def test_login():
    print "Test Login"
    try:
        cl.login("administrator", "hpinvent")
        pprint.pprint("Login worked")
    except exceptions.HTTPUnauthorized:
        pprint.pprint("Login Failed")


def test_logout():
    print "Test Logout"
    try:
        cl.login("administrator", "hpinvent")
        pprint.pprint("Login worked")
    except exceptions.HTTPUnauthorized:
        pprint.pprint("Login Failed")

    try:
        cl.logout()
        pprint.pprint("Logout worked")
    except exceptions.HTTPUnauthorized:
        pprint.pprint("Logout Failed")


def test_get_snapshot(snap_id):
    print "Get Snapshot"
    try:
        cl.login("administrator", "hpinvent")
        snap = cl.getSnapshot(snap_id)
        pprint.pprint(snap)
    except exceptions.HTTPUnauthorized as ex:
        pprint.pprint("You must login first")
    except Exception as ex:
        pprint.pprint(ex)


def test_get_snapshot_by_name(name):
    print "Get Snapshot By Name"
    try:
        cl.login("administrator", "hpinvent")
        snap = cl.getSnapshotByName(name)
        pprint.pprint(snap)
    except exceptions.HTTPUnauthorized as ex:
        pprint.pprint("You must login first")
    except Exception as ex:
        pprint.pprint(ex)


def test_create_snapshot():
    print "Create Snapshot"
    try:
        cl.login("administrator", "hpinvent")
        vol = cl.createVolume("VolumeSource", 20, 1048576)
        snapshot = cl.createSnapshot('VolumeSnapshot', vol['id'])
        pprint.pprint(snapshot)
        cl.deleteSnapshot(snapshot['id'])
        cl.deleteVolume(vol['id'])
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_snapshots():
    print "Get Snapshots"
    try:
        cl.login("administrator", "hpinvent")
        snapshots = cl.getSnapshots()
        pprint.pprint(snapshots)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_servers():
    print "Get Servers"
    try:
        cl.login("administrator", "hpinvent")
        servers = cl.getServers()
        pprint.pprint(servers)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_server(server_id):
    print "Get Server"
    try:
        cl.login("administrator", "hpinvent")
        server = cl.getServer(server_id)
        pprint.pprint(server)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_server_by_name(name):
    print "Get Server By Name"
    try:
        cl.login("administrator", "hpinvent")
        server = cl.getServerByName(name)
        pprint.pprint(server)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_volume(volume_id):
    print "Get Volumes"
    try:
        cl.login("administrator", "hpinvent")
        volume = cl.getVolume(volume_id)
        return volume
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_volume_by_name(name):
    print "Get Volume By Name"
    try:
        cl.login("administrator", "hpinvent")
        volume = cl.getVolumeByName(name)
        return volume
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_volumes():
    print "Get Volumes"
    try:
        cl.login("administrator", "hpinvent")
        volumes = cl.getVolumes()
        pprint.pprint(volumes)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_clusters():
    print "Get Clusters"
    try:
        cl.login("administrator", "hpinvent")
        volumes = cl.getClusters()
        pprint.pprint(volumes)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_get_cluster_by_name(name):
    print "Get Cluster By Name"
    try:
        cl.login("administrator", "hpinvent")
        volumes = cl.getClusterByName(name)
        pprint.pprint(volumes)
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_create_volume():
    print "Create Volumes"
    try:
        cl.login("administrator", "hpinvent")
        vol = cl.createVolume("Volume1", 20, 1048576)
        return vol

    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_delete_volume(volume_id):
    print "Delete a Volume"
    try:
        cl.login("administrator", "hpinvent")
        vol = cl.deleteVolume(volume_id)
        return vol
    except exceptions.HTTPUnauthorized:
        pprint.pprint("You must login first")


def test_error():
    print "test Error"
    try:
        cl.login("administrator", "hpinvent")
        resp, body = cl.http.get('/throwerror')
        pprint.pprint(resp)
        pprint.pprint(body)
    except Exception as ex:
        print ex

#test_login()
#test_logout()

#vols = test_get_volumes()
#vol = test_get_volume_by_name("vol1_test")
#vols = test_get_clusters()

#snap = test_get_snapshot("25")
#snap = test_get_snapshot_by_name("vol1_test_SS_1")
snaps = test_get_snapshots()

#clusters = test_get_clusters()
#cluster = test_get_cluster_by_name("ClusterVSA309")

#servers = test_get_servers()
#server = test_get_server_by_name("jim-devstack")

#vol = test_get_volume(23)
#pprint.pprint(vol)

#test_delete_volume(400)

#test_create_snapshot()

#test_error()
