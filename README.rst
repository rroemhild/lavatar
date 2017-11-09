Lavatar
=======

Lavatar is an LDAP-backend avatar server with `Gravatar <https://secure.gravatar.com/site/implement>`_ like URL support.

Lavatar fetches all email addresses from an LDAP server with a given search filter and stores them with their md5hash on Redis. Per defualt Lavatar also use Redis to cache the avatar images.

For now lavatar only support image requests.

Quick start
-----------

You can use the docker container image and the docker-compose example to test this app:

.. code-block:: shell

    wget https://raw.githubusercontent.com/rroemhild/lavatar/master/docker-compose.yml
    docker-compose up

and test in browser: http://localhost:5000/avatar/982391f62e589420d9fdb56a62c5e16c

Install
-------

.. code-block:: shell

    git clone https://github.com/rroemhild/lavatar.git
    cd lavatar
    pip install -r requirements.txt gevent
    cp lavatar/default_settings.py settings.py

Configure lavatar in settings.py and run ``python production.py`` example.

Image Request
-------------

The default image size for the base request is 80x80, max size limit is 1024x1024.

.. code-block:: shell

    http://localhost:5000/avatar/HASH

Set ``s`` or ``size`` to scale the avatar image

.. code-block:: shell

    http://localhost:5000/avatar/HASH?s=160

Set ``d`` or ``default`` for the default image available in ``static/img``.

.. code-block:: shell

    http://localhost:5000/avatar/HASH?d=keyword

Set ``m`` or ``method`` to resize Image with the specified method: 'crop', 'cover', 'contain', 'width', 'height' or 'thumbnail'. Default is ``thumbnail``

.. code-block:: shell

    http://localhost:5000/avatar/HASH?s=120&m=cover

Set ``w`` or ``width`` to resize width and ``h`` or ``height`` to resize height.

.. code-block:: shell

    http://localhost:5000/avatar/HASH?h=120&m=height
