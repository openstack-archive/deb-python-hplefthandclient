# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2012 Hewlett Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
HPLeftHand REST Client

.. module: HPLeftHandClient
.. moduleauthor: Kurt Martin

:Author: Kurt Martin
:Description: This is the LeftHand/StoreVirtual Client that talks to the
LeftHand OS REST Service.

This client requires and works with version 11.5 of the LeftHand firmware

"""

try:
    # For Python 3.0 and later
    from urllib.parse import quote
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import quote

from hplefthandclient import exceptions, http


class HPLeftHandClient:

    # Minimum API version needed for consistency group support
    MIN_CG_API_VERSION = '1.2'

    def __init__(self, api_url, debug=False, secure=False):
        self.api_url = api_url
        self.http = http.HTTPJSONRESTClient(self.api_url, secure=secure)
        self.api_version = None

        self.debug_rest(debug)

    def debug_rest(self, flag):
        """
        This is useful for debugging requests to LeftHand

        :param flag: set to True to enable debugging
        :type flag: bool

        """
        self.http.set_debug_flag(flag)

    def login(self, username, password):
        """
        This authenticates against the LH OS REST server and creates a session.

        :param username: The username
        :type username: str
        :param password: The password
        :type password: str

        :returns: None

        """
        try:
            resp = self.http.authenticate(username, password)
            self.api_version = resp['x-api-version']
        except Exception as ex:
            ex_desc = ex.get_description()

            if (ex_desc and ("Unable to find the server at" in ex_desc or
                             "Only absolute URIs are allowed" in ex_desc)):
                raise exceptions.HTTPBadRequest(ex_desc)
            if (ex_desc and "SSL Certificate Verification Failed" in ex_desc):
                raise exceptions.SSLCertFailed()
            else:
                msg = ('Error: \'%s\' - Error communicating with the LeftHand '
                       'API. Check proxy settings. If error persists, either '
                       'the LeftHand API is not running or the version of the '
                       'API is not supported.') % ex_desc
                raise exceptions.UnsupportedVersion(msg)

    def logout(self):
        """
        This destroys the session and logs out from the LH OS server

        :returns: None

        """
        self.http.unauthenticate()

    def getApiVersion(self):
        """
        This retrieves the API version of the backend.

        :returns:  REST API Version
        """
        return self.api_version

    def getClusters(self):
        """
        Get the list of Clusters

        :returns: list of Clusters
        """
        response, body = self.http.get('/clusters')
        return body

    def getCluster(self, cluster_id):
        """
        Get information about a Cluster

        :param cluster_id: The id of the cluster to find
        :type cluster_id: str

        :returns: cluster
        """
        response, body = self.http.get('/clusters/%s' % cluster_id)
        return body

    def getClusterByName(self, name):
        """
        Get information about a cluster by name

        :param name: The name of the cluster to find
        :type name: str

        :returns: cluster
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_CLUSTER - cluster doesn't exist
        """
        response, body = self.http.get('/clusters?name=%s' % name)
        return body

    def getServers(self):
        """
        Get the list of Servers

        :returns: list of Servers
        """
        response, body = self.http.get('/servers')
        return body

    def getServer(self, server_id):
        """
        Get information about a server

        :param server_id: The id of the server to find
        :type server_id: str

        :returns: server
        :raises: :class:`~hplefthandclient.exceptions.HTTPServerError`
        """
        response, body = self.http.get('/servers/%s' % server_id)
        return body

    def getServerByName(self, name):
        """
        Get information about a server by name

        :param name: The name of the server to find
        :type name: str

        :returns: server
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_SERVER - server doesn't exist
        """
        response, body = self.http.get('/servers?name=%s' % name)
        return body

    def createServer(self, name, iqn, optional=None):
        """
        Create a server by name

        :param name: The name of the server to create
        :type name: str
        :param iqn: The iSCSI qualified name
        :type name: str
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python

            optional = {
                'description' : "some comment",
                'iscsiEnabled' : True,
                'chapName': "some chap name",
                'chapAuthenticationRequired': False,
                'chapInitiatorSecret': "initiator secret",
                'chapTargetSecret': "target secret",
                'iscsiLoadBalancingEnabled': True,
                'controllingServerName': "server name",
                'fibreChannelEnabled': False,
                'inServerCluster": True
            }

        :returns: server
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_SERVER - server doesn't exist
        """
        info = {'name': name, 'iscsiIQN': iqn}
        if optional:
            info = self._mergeDict(info, optional)

        response, body = self.http.post('/servers', body=info)
        return body

    def deleteServer(self, server_id):
        """
        Delete a Server

        :param server_id: the server ID to delete

        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_SERVER - The server does not exist
        """
        response, body = self.http.delete('/servers/%s' % server_id)
        return body

    def getSnapshots(self):
        """
        Get the list of Snapshots

        :returns: list of Snapshots
        """
        response, body = self.http.get('/snapshots')
        return body

    def getSnapshot(self, snapshot_id):
        """
        Get information about a Snapshot

        :returns: snapshot
        :raises: :class:`~hplefthandclient.exceptions.HTTPServerError`
        """
        response, body = self.http.get('/snapshots/%s' % snapshot_id)
        return body

    def getSnapshotByName(self, name):
        """
        Get information about a snapshot by name

        :param name: The name of the snapshot to find

        :returns: volume
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_SNAP - shapshot doesn't exist
        """
        response, body = self.http.get('/snapshots?name=%s' % name)
        return body

    def createSnapshot(self, name, source_volume_id, optional=None):
        """
        Create a snapshot of an existing Volume

        :param name: Name of the Snapshot
        :type name: str
        :param source_volume_id: The volume you want to snapshot
        :type source_volume_id: int
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python

            optional = {
                'description' : "some comment",
                'inheritAccess' : false
            }

        """
        parameters = {'name': name}
        if optional:
            parameters = self._mergeDict(parameters, optional)

        info = {'action': 'createSnapshot',
                'parameters': parameters}

        response, body = self.http.post('/volumes/%s' % source_volume_id,
                                        body=info)
        return body

    def createSnapshotSet(self, source_volume_id, snapshot_set,
                          optional=None):
        """
        Create a snapshot of multiple existing volumes

        :param source_volume_id: The base volume you want to snapshot. NOTE:
                                 Must be the ID of the first volume listed in
                                 snapshot_set.
        :type source_volume_id: int
        :param snapshot_set: Array of SnapshotSet entities. The 1st entry
                             of the array will always be the current volume.
        :type snapshot_set: Array
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python
            snapshotSet = [
                {
                    "volumeName": "myVol1",
                    "volumeId": 48,
                    "snapshotName": "myVolSnapshot-0"
                },
                {
                    "volumeName": "myVol2",
                    "volumeId": 58,
                    "snapshotName": "myVolSnapshot-1"
                }
            ]

            optional = {
                'description' : "some comment",
                'inheritAccess' : false
            }

        """
        # we need to be on LeftHand API version 1.2 to create a snapshot set
        if self.api_version < self.MIN_CG_API_VERSION:
            ex_msg = ('Invalid LeftHand API version found (%(found)s).'
                      'Version %(minimum)s or greater required.') % {
                'found': self.api_version,
                'minimum': self.MIN_CG_API_VERSION}
            raise exceptions.UnsupportedVersion(ex_msg)

        parameters = {'snapshotSet': snapshot_set}
        if optional:
            parameters = self._mergeDict(parameters, optional)

        info = {'action': 'createSnapshotSet',
                'parameters': parameters}

        response, body = self.http.post('/volumes/%s' % source_volume_id,
                                        body=info)
        return body

    def deleteSnapshot(self, snapshot_id):
        """
        Delete a Snapshot

        :param snapshot_id: the snapshot ID to delete

        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_SNAPSHOT - The snapshot does not exist
        """
        response, body = self.http.delete('/snapshots/%s' % snapshot_id)
        return body

    def cloneSnapshot(self, name, source_snapshot_id, optional=None):
        """
        Create a clone of an existing Shapshot

        :param name: Name of the Snapshot clone
        :type name: str
        :param source_snapshot_id: The snapshot you want to clone
        :type source_snapshot_id: int
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python

            optional = {
                'description' : "some comment"
            }

        """
        parameters = {'name': name}
        if optional:
            parameters = self._mergeDict(parameters, optional)

        info = {'action': 'createSmartClone',
                'parameters': parameters}

        response, body = self.http.post('/snapshots/%s' % source_snapshot_id,
                                        body=info)
        return body

    def getVolumes(self, cluster=None, fields=None):
        """
        Get the list of Volumes

        :param cluster: a cluster name
        :type cluster: str
        :param fields: specific fields of the returning data
        :type fields: list

        :returns: list of Volumes
        """
        fieldsQuery = []
        query = None
        if fields:
            tmpFields = []
            for field in fields:
                tmpFields.append(field)
            fieldsQuery = ('%s' % ','.join(tmpFields))

        if cluster and fieldsQuery:
            query = ('clusterName=%(cluster)s&fields=%(fieldsQuery)s' %
                     ({'cluster': quote(cluster.encode('utf8')),
                       'fieldsQuery': fieldsQuery}))
        elif cluster:
            # clusterName is documented, but not working, at this
            # point will get everything
            query = 'clusterName=%s' % quote(cluster.encode('utf8'))
        elif fieldsQuery:
            query = 'fields=%s' % fieldsQuery

        url = '/volumes'
        if query:
            url = '/volumes?%s' % query

        response, body = self.http.get(url)

        # Workaround for clusterName doesn't work in current API
        if cluster and fields and 'members[clusterName]' in fields:
            all_members = body['members']
            cluster_members = [member for member in all_members
                               if member['clusterName'] == cluster]
            body['members'] = cluster_members
            body['total'] = len(cluster_members)

        return body

    def getVolume(self, volume_id, query=None):
        """
        Get information about a volume

        :param volume_id: The id of the volume to find
        :param query: Optional query parameter, e.g. fields, expand-links
        :type volume_id: str

        :returns: volume
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_VOL - volume doesn't exist
        """
        uri = '/volumes/%s' % volume_id
        if query:
            uri = uri + '?' + query
        response, body = self.http.get(uri)
        return body

    def getVolumeByName(self, name):
        """
        Get information about a volume by name

        :param name: The name of the volume to find
        :type name: str

        :returns: volume
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_VOL - volume doesn't exist
        """
        response, body = self.http.get('/volumes?name=%s' % name)
        return body

    def findServerVolumes(self, server_name):
        """Find volumes that are exported to a server.

        :param server_name: The name of the server to search.
        :type server_name: str

        :returns: A list of volumes that are on the specified server.
        """

        # The only mechanism we have in 1.0 of the REST API
        # is to fetch all volumes and filter through them.
        # So we limit the return fields to cut down on the
        # n/w usage.
        # TODO(walter-boring)
        response, body = self.http.get(
            '/volumes?fields=members[name],members[volumeACL]')

        # Creates a list of volumes that have read/write access to the
        # specified server.
        volumes = [
            self.getVolumeByName(volume['name'])
            # Filter out volumes that do not have the volumeACL property set.
            for volume in body['members']
            if ('volumeACL' in volume and
                volume['volumeACL'] is not None)
            # Filter out volumes that do not have access to the target server.
            for entry in volume['volumeACL']
            if ('server' in entry and
                entry['server']['name'] == server_name)
        ]

        return volumes

    def createVolume(self, name, cluster_id, size, optional=None):
        """ Create a new volume

        :param name: the name of the volume
        :type name: str
        :param cluster_id: the cluster Id
        :type cluster_id: int
        :param sizeKB: size in KB for the volume
        :type sizeKB: int
        :param optional: dict of other optional items
        :type optional: dict

        .. code-block:: python

            optional = {
             'description': 'some comment',
             'isThinProvisioned': 'true',
             'autogrowSeconds': 200,
             'clusterName': 'somename',
             'isAdaptiveOptimizationEnabled': 'true',
             'dataProtectionLevel': 2,
            }

        :returns: List of Volumes

        :raises: :class:`~hplefthandclient.exceptions.HTTPConflict`
            - EXISTENT_SV - Volume Exists already
        """
        info = {'name': name, 'clusterId': cluster_id, 'size': size}
        if optional:
            info = self._mergeDict(info, optional)

        response, body = self.http.post('/volumes', body=info)
        return body

    def deleteVolume(self, volume_id):
        """
        Delete a volume

        :param name: the name of the volume
        :type name: str

        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_VOL - The volume does not exist
        """
        response, body = self.http.delete('/volumes/%s' % volume_id)
        return body

    def modifyVolume(self, volume_id, optional):
        """Modify an existing volume.

        :param volume_id: The id of the volume to find
        :type volume_id: str

        :returns: volume
        :raises: :class:`~hplefthandclient.exceptions.HTTPNotFound`
            - NON_EXISTENT_VOL - volume doesn't exist
        """
        info = {'volume_id': volume_id}
        info = self._mergeDict(info, optional)
        response, body = self.http.put('/volumes/%s' % volume_id, body=info)
        return body

    def cloneVolume(self, name, source_volume_id, optional=None):
        """
        Create a clone of an existing Volume

        :param name: Name of the Volume clone
        :type name: str
        :param source_volume_id: The Volume you want to clone
        :type source_volume_id: int
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python

            optional = {
                'description' : "some comment"
            }

        """
        parameters = {'name': name}
        if optional:
            parameters = self._mergeDict(parameters, optional)

        info = {'action': 'createSmartClone',
                'parameters': parameters}

        response, body = self.http.post('/volumes/%s' % source_volume_id,
                                        body=info)
        return body

    def addServerAccess(self, volume_id, server_id, optional=None):
        """
        Assign a Volume to a Server

        :param volume_id: Volume ID of the volume
        :type name: int
        :param server_id: Server ID of the server to add the volume to
        :type source_volume_id: int
        :param optional: Dictionary of optional params
        :type optional: dict

        .. code-block:: python

            optional = {
                'Transport' : 0,
                'Lun' : 1,
            }

        """
        parameters = {'serverID': server_id,
                      'exclusiveAccess': True,
                      'readAccess': True,
                      'writeAccess': True}
        if optional:
            parameters = self._mergeDict(parameters, optional)

        info = {'action': 'addServerAccess',
                'parameters': parameters}

        response, body = self.http.post('/volumes/%s' % volume_id,
                                        body=info)
        return body

    def removeServerAccess(self, volume_id, server_id):
        """
        Unassign a Volume from a Server

        :param volume_id: Volume ID of the volume
        :type name: int
        :param server_id: Server ID of the server to remove the volume fom
        :type source_volume_id: int

        """
        parameters = {'serverID': server_id}

        info = {'action': 'removeServerAccess',
                'parameters': parameters}

        response, body = self.http.post('/volumes/%s' % volume_id,
                                        body=info)
        return body

    def _mergeDict(self, dict1, dict2):
        """
        Safely merge 2 dictionaries together

        :param dict1: The first dictionary
        :type dict1: dict
        :param dict2: The second dictionary
        :type dict2: dict

        :returns: dict

        :raises Exception: dict1, dict2 is not a dictionary
        """
        if type(dict1) is not dict:
            raise Exception("dict1 is not a dictionary")
        if type(dict2) is not dict:
            raise Exception("dict2 is not a dictionary")

        dict3 = dict1.copy()
        dict3.update(dict2)
        return dict3
