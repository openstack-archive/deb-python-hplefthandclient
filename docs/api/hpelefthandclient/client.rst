:mod:`client` -- HPELeftHandClient
=================================

.. automodule:: hpelefthandclient.client
   :synopsis: HPE LeftHand REST Web client

   .. autoclass:: hpelefthandclient.client.HPELeftHandClient(api_url, secure=False)

      .. automethod:: debug_rest
      .. automethod:: login
      .. automethod:: logout
      .. automethod:: getClusters
      .. automethod:: getCluster
      .. automethod:: getClusterByName
      .. automethod:: getServers
      .. automethod:: getServer
      .. automethod:: getServerByName
      .. automethod:: createServer
      .. automethod:: deleteServer
      .. automethod:: getSnapshots
      .. automethod:: getSnapshot
      .. automethod:: getSnapshotByName
      .. automethod:: createSnapshot
      .. automethod:: deleteSnapshot
      .. automethod:: cloneSnapshot
      .. automethod:: modifySnapshot
      .. automethod:: getVolumes
      .. automethod:: getVolume
      .. automethod:: getVolumeByName
      .. automethod:: findServerVolumes
      .. automethod:: createVolume
      .. automethod:: deleteVolume
      .. automethod:: modifyVolume
      .. automethod:: cloneVolume
      .. automethod:: addServerAccess
      .. automethod:: removeServerAccess
      .. automethod:: makeVolumeRemote
      .. automethod:: makeVolumePrimary
      .. automethod:: createRemoteSnapshotSchedule
      .. automethod:: deleteRemoteSnapshotSchedule
      .. automethod:: getRemoteSnapshotSchedule
      .. automethod:: stopRemoteSnapshotSchedule
      .. automethod:: startRemoteSnapshotSchedule
      .. automethod:: doesRemoteSnapshotScheduleExist
      .. automethod:: getIPFromCluster
