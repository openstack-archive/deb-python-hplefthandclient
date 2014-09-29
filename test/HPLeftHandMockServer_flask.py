import pprint
import json
import random
import string
import argparse
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from flask import Flask, request, make_response, session, abort, Response

parser = argparse.ArgumentParser()
parser.add_argument("-debug", help="Turn on http debugging",
                    default=False, action="store_true")
parser.add_argument("-user", help="User name", default='administrator')
parser.add_argument("-password", help="User password", default='hpinvent')
parser.add_argument("-port", help="Port to listen on", type=int, default=5001)
args = parser.parse_args()
user_name = args.user
user_pass = args.password
debugRequests = False
if "debug" in args and args.debug is True:
    debugRequests = True

#__all__ = ['make_json_app']


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        pprint.pprint(ex)
        pprint.pprint(ex.code)
        #response = jsonify(message=str(ex))
        response = json.dumps(ex)
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)
    #app.debug = True
    app.secret_key = id_generator(24)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)

session_key = id_generator(24)


def debugRequest(request):
    if debugRequests:
        print "\n"
        pprint.pprint(request)
        pprint.pprint(request.headers)
        pprint.pprint(request.data)


def throw_error(http_code, error_code=None,
                desc=None, debug1=None, debug2=None):
    if error_code:
        info = {'code': error_code, 'desc': desc}
        if debug1:
            info['debug1'] = debug1
        if debug2:
            info['debug2'] = debug2
        abort(Response(json.dumps(info), status=http_code))
    else:
        abort(http_code)


@app.route('/')
def index():
    debugRequest(request)
    if 'username' in session:
        return 'Logged in as %s' % session['username']
    abort(401)


@app.route('/lhos/throwerror')
def errtest():
    debugRequest(request)
    throw_error(405, 'ERR_TEST', 'testing throwing an error',
                'debug1 message', 'debug2 message')


@app.errorhandler(404)
def not_found(error):
    debugRequest(request)
    return Response("%s has not been implemented" % request.path, status=501)


@app.route('/lhos/credentials', methods=['GET', 'POST'])
def credentials():
    debugRequest(request)

    if request.method == 'GET':
        return 'GET credentials called'

    elif request.method == 'POST':
        data = json.loads(request.data)

        if data['user'] == user_name and data['password'] == user_pass:
            #do something good here
            try:
                resp = make_response(json.dumps({'key': session_key}), 201)
                resp.headers['Location'] = '/lhos/credentials/%s' % session_key
                session['username'] = data['user']
                session['password'] = data['password']
                session['session_key'] = session_key
                return resp
            except Exception as ex:
                pprint.pprint(ex)

        else:
            #authentication failed!
            throw_error(401, "HTTP_AUTH_FAIL",
                        "Username and or Password was incorrect")


@app.route('/lhos/credentials/<session_key>', methods=['DELETE'])
def logout_credentials(session_key):
    debugRequest(request)
    session.clear()
    return 'DELETE credentials called'

#### CLUSTER INFO ####


@app.route('/lhos/clusters', methods=['GET'])
def get_cluster_by_name():
    debugRequest(request)
    cluster_name = request.args.get('name')

    for cluster in clusters['members']:
        if cluster['name'] == cluster_name:
            resp = make_response(json.dumps(cluster), 200)
            return resp

    throw_error(404, 'NON_EXISTENT_CLUSTER', "cluster doesn't exist")

### SERVERS ####


@app.route('/lhos/servers', methods=['POST'])
def create_server():
    debugRequest(request)
    data = json.loads(request.data)

    if 'name' not in data.keys() or data['name'] is None:
        throw_error(400, 'INVALID_USER_INPUT', 'No server name provided.')

    if 'iscsiIQN' not in data.keys() or data['iscsiIQN'] is None:
        throw_error(500, 'SERVER_ERROR', 'No iscsiIQN provided.')

    for server in servers['members']:
        if data['name'] == server['name']:
            throw_error(500, 'SERVER_ERROR', 'The server already exists.')

    data['id'] = random.randint(1, 2000)

    servers['members'].append(data)
    servers['total'] += 1
    return make_response("", 201)


@app.route('/lhos/servers/<server_id>', methods=['DELETE'])
def delete_server(server_id):
    debugRequest(request)

    for server in servers['members']:
        if server['id'] == int(server_id):
            servers['members'].remove(server)
            servers['total'] -= 1
            return make_response("", 200)

    throw_error(500, 'SERVER_ERROR',
                "The server id '%s' does not exists." % server_id)


@app.route('/lhos/servers', methods=['GET'])
def get_server():
    debugRequest(request)
    server_name = None
    server_name = request.args.get('name')

    if server_name is not None:
        for server in servers['members']:
            if server['name'] == server_name:
                resp = make_response(json.dumps(server), 200)
                return resp
        throw_error(404, 'NON_EXISTENT_VOLUME', "server doesn't exist")
    else:
        resp = make_response(json.dumps(servers), 200)
        return resp


### VOLUMES & SNAPSHOTS ####


@app.route('/lhos/volumes/<volume_id>', methods=['POST'])
def handle_volume_actions(volume_id):
    debugRequest(request)
    data = json.loads(request.data)

    valid_keys = {'serverID': None, 'parameters': None,
                  'exclusiveAccess': None,
                  'readAccess': None, 'writeAccess': None, 'action': None,
                  'transport': None, 'lun': None}

    for key in data.keys():
        if key not in valid_keys.keys():
            throw_error(400, 'BAD_REQUEST', "Invalid Parameter '%s'" % key)

    # Checking if volume exists.
    volume = next(
        (vol for vol in volumes['members'] if vol['id'] == int(volume_id)),
        None
    )

    if volume is None:
        throw_error(500, 'VOLUME_ID_NOT_FOUND', "volume doesn't exist")

    # The server_id parameter is only present for some actions so it needs
    # to be checked for existence.
    server_id = None
    if data['parameters'] is not None and 'serverID' in data['parameters']:
        server_id = data['parameters']['serverID']

        if server_id < 0:
            throw_error(400, 'INVALID_USER_INPUT', 'Server ID is invalid.')

        # Checking if server exists.
        server = next(
            (serv for serv in servers['members'] if serv['id'] == server_id),
            None
        )

        if server is None:
            throw_error(500, 'SERVER_ID_NOT_FOUND', "server doesn't exist")

    if data['action'] == "addServerAccess":
        # Initialize the volumeACL property if it doesn't exist, otherwise
        # make sure the server access isn't already added for this volume.
        if volume['volumeACL'] is None:
            volume['volumeACL'] = []
        else:
            existing_server = next(
                (item for item in volume['volumeACL']
                 if item['server']['name'] == server['name']),
                None
            )
            if existing_server is not None:
                throw_error(500,
                            'SERVER_ERROR',
                            'Server access already added.')

        # Enable server access for this volume.
        server_info = {
            'server': {
                'name': server['name'],
                'uri': '/lhos/servers/' + str(server['id'])
            }
        }
        volume['volumeACL'].append(server_info)
    elif data['action'] == "removeServerAccess":
        # Find the server and remove the access from the volume.  If this is
        # the last access for the volume, reset the volumeACL property to None.
        # Do nothing if the server access doesn't exist.
        if volume['volumeACL'] is not None:
            for i, item in enumerate(volume['volumeACL']):
                if item['server']['name'] == server['name']:
                    volume['volumeACL'].pop(i)
                    if len(volume['volumeACL']) == 0:
                        volume['volumeACL'] = None
                    break
    elif data['action'] == "createSnapshot":
        snapshots['members'].append({'name': data['parameters'].get('name'),
                                     'id': random.randint(1, 2000)})
        pprint.pprint(snapshots)
    else:
        throw_error(500, 'SERVER_ERROR', 'Action does not exist.')

    return make_response("", 200)


@app.route('/lhos/volumes', methods=['GET'])
def get_volume():
    debugRequest(request)
    volume_name = None
    volume_name = request.args.get('name')

    if volume_name is not None:
        for volume in volumes['members']:
            if volume['name'] == volume_name:
                resp = make_response(json.dumps(volume), 200)
                return resp
        throw_error(404, 'NON_EXISTENT_VOLUME', "volume doesn't exist")
    else:
        resp = make_response(json.dumps(volumes), 200)
        return resp


@app.route('/lhos/snapshots', methods=['GET'])
def get_snapshot():
    debugRequest(request)
    snapshot_name = None
    snapshot_name = request.args.get('name')

    if snapshot_name is not None:
        pprint.pprint('snapshot name %s' % snapshot_name)
        for snapshot in snapshots['members']:
            if snapshot['name'] == snapshot_name:
                pprint.pprint('snapshot name inside %s' % snapshot['name'])
                resp = make_response(json.dumps(snapshot), 200)
                return resp
        throw_error(404, 'NON_EXISTENT_SNAPSHOT', "snapshot doesn't exist")
    else:
        resp = make_response(json.dumps(snapshots), 200)
        return resp


@app.route('/lhos/volumes', methods=['POST'])
def create_volumes():
    debugRequest(request)
    data = json.loads(request.data)

    valid_keys = {'name': None, 'isThinProvisioned': None, 'size': None,
                  'description': None, 'clusterID': None}

    for key in data.keys():
        if key not in valid_keys.keys():
            throw_error(500, 'SERVER_ERROR', "Invalid Parameter '%s'" % key)

    if 'name' in data.keys():
        for vol in volumes['members']:
            if vol['name'] == data['name']:
                throw_error(500, 'SERVER_ERROR',
                            'The volume already exists.')
    else:
        throw_error(500, 'SERVER_ERROR',
                    'No volume name provided.')

    if 'size' in data.keys():
        if data['size'] > 17592188141567:
            throw_error(500, 'SERVER_ERROR', 'Volume to larger')

    data['id'] = random.randint(1, 2000)
    data['volumeACL'] = None

    volumes['members'].append(data)
    return make_response("", 200)


@app.route('/lhos/volumes/<volume_id>', methods=['DELETE'])
def delete_volumes(volume_id):
    debugRequest(request)
    for volume in volumes['members']:
        if volume['id'] == int(volume_id):
            volumes['members'].remove(volume)
            return make_response("", 200)

    throw_error(500, 'SERVER_ERROR',
                "The volume id '%s' does not exists." % volume_id)


@app.route('/lhos/snapshots/<snapshot_id>', methods=['DELETE'])
def delete_snapshots(snapshot_id):
    debugRequest(request)
    for snapshot in snapshots['members']:
        if snapshot['id'] == int(snapshot_id):
            snapshots['members'].remove(snapshot)
            return make_response("", 200)

    throw_error(404, 'NON_EXISTENT_SNAPSHOT',
                "The snapshot id '%s' does not exists." % snapshot_id)


if __name__ == "__main__":

    #fake  volumes
    global volumes
    volumes = {'members': [{
               'autogrowSeconds': 2,
               'bytesWritten': 0,
               'clusterId': 21,
               'clusterName': 'ClusterVSA309',
               'created': '2013-10-23T16:58:58Z',
               'dataProtectionLevel': 0,
               'dataWritten': 0,
               'description': 'test volume',
               'fcTransportStatus': 0,
               'fibreChannelPaths': None,
               'friendlyName': '',
               'hasUnrecoverableIOErrors': False,
               'id': 24,
               'isAdaptiveOptimizationEnabled': True,
               'isAvailable': True,
               'isDeleting': False,
               'isLicensed': True,
               'isMigrating': False,
               'isPrimary': True,
               'isThinProvisioned': False,
               'isVIPRebalancing': False,
               'iscsiIqn': 'iqn.2003-10.com.lefthandnetworks:mgvsa309:24:vol1',
               'iscsiSessions': None,
               'migrationStatus': 'none',
               'modified': '',
               'name': 'VOLUME0_UNIT_TEST',
               'numberOfReplicas': 1,
               'provisionedSpace': 4194304,
               'replicationStatus': 'normal',
               'restripePendingStatus': 'none',
               'resynchronizationStatus': 'none',
               'scsiLUNStatus': 'available',
               'serialNumber': '27d18c785f81e91f36a5073fff92337\
                                20000000000000018',
               'size': 1048576,
               'snapshots': {'name': 'snapshots',
                             'resource': None,
                             'type': 'snapshot',
                             'uri': '/snapshots?volumeName=VOLUME1_UNIT_TEST'},
               'transport': 0,
               'transportServerId': 0,
               'type': 'volume',
               'uri': '/lhos/volumes/24',
               'volumeACL': None}],
               'total': 4}

    #fake snapshots
    global snapshots
    snapshots = {'members': [{
                 'autogrowSeconds': 2,
                 'bytesWritten': 0,
                 'clusterId': 21,
                 'clusterName': 'ClusterVSA309',
                 'created': '2013-10-23T16:59:19Z',
                 'dataWritten': 0,
                 'description': '',
                 'fcTransportStatus': 0,
                 'fibreChannelPaths': None,
                 'hasUnrecoverableIOErrors': False,
                 'id': 26,
                 'isAutomatic': False,
                 'isAvailable': True,
                 'isDeleting': False,
                 'isLicensed': True,
                 'isMigrating': False,
                 'isPrimary': True,
                 'isThinProvisioned': True,
                 'iscsiIqn':
                     'iqn.2003-10.com.lefthandnetworks:mgvsa309:26:vol1-ss-1',
                 'managedBy': 0,
                 'migrationStatus': 'none',
                 'modified': '',
                 'name': 'vol1_SS_1',
                 'provisionedSpace': 528384,
                 'replicationStatus': 'normal',
                 'restripePendingStatus': 'none',
                 'resynchronizationStatus': 'none',
                 'scsiLUNStatus': 'available',
                 'serialNumber':
                     '27d18c785f81e91f36a5073fff923372000000000000001a',
                 'sessions': None,
                 'size': 4194304,
                 'snapshotACL': None,
                 'transport': 0,
                 'transportServerId': 0,
                 'type': 'snapshot',
                 'uri': '/lhos/snapshots/26',
                 'writableSpaceUsed': 0}],
                 'total': 4}

    #fake clusters
    global clusters
    clusters = {'members': [{
                'adaptiveOptimizationCapable': False,
                'created': 'N/A',
                'description': '',
                'id': 21,
                'modified': 'N/A',
                'moduleCount': 1,
                'name': 'ClusterVSA309',
                'spaceAvailable': 13457408,
                'spaceTotal': 40728576,
                'storageModuleIPAddresses': ['10.10.30.165'],
                'supportedFeatures': [''],
                'type': 'cluster',
                'uri': '/lhos/clusters/21',
                'virtualIPAddresses': [{'ipV4Address': '10.10.22.7',
                                        'ipV4NetMask': '255.255.224.0'}],
                'virtualIPEnabled': True,
                'volumeCreationSpace': [{'availableSpace': 13457408,
                                         'replicationLevel': 1}],
                'volumes': {'name': 'volumes',
                            'resource': None,
                            'type': 'volume',
                            'uri': '/volumes?clusterName=ClusterVSA309'}}],
                'name': 'Clusters Collection',
                'total': 1,
                'type': 'cluster',
                'uri': '/lhos/clusters'}

    #fake servers
    global servers
    servers = {'members': [], 'total': 0}

    app.run(port=args.port, debug=debugRequests)
