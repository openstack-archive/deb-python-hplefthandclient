:mod:`http` -- HTTP REST Base Class
====================================================

.. automodule:: hplefthandclient.http
   :synopsis: HTTP REST Base Class

   .. autoclass::hplefthandclient.http(api_url, [insecure=False[,http_log_debug=False]])

      .. automethod:: authenticate
      .. automethod:: unauthenticate

      .. describe:: c[db_name] || c.db_name

         Get the `db_name` :class:`~pymongo.database.Database` on :class:`Connection` `c`.

         Raises :class:`~pymongo.errors.InvalidName` if an invalid database name is used.

      .. autoattribute:: api_url
      .. autoattribute:: http_log_debug
      .. automethod:: request
      .. automethod:: get
      .. automethod:: post
      .. automethod:: put
      .. automethod:: delete
