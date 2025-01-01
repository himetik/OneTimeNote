Local Setup Instructions
============================


Project Setup
-------------

Before running this app make sure you have installed Docker Compose.

`Docker Installation Guide <https://docs.docker.com/engine/install/>`_

`Docker Compose Installation Guide <https://docs.docker.com/compose/install/>`_

Cloning a Remote Repository
--------

.. code-block:: sh

    git clone git@github.com:himetik/onetimenote.git

Starting a Virtual Environment
--------

.. code-block:: sh

    cd onetimenote && python3 -m venv venv && source venv/bin/activate

Implementation of Environment Variables
--------

.. code-block:: sh

    # use .env.example as instance
    touch .env

Container Management
--------

Launching containers
~~~~~~~~

.. code-block:: sh

    docker-compose up -d

Stopping containers
~~~~~~~~

.. code-block:: sh

    docker-compose down

View container logs
~~~~~~~~

.. code-block:: sh

    docker-compose logs -f

Entering the container
~~~~~~~~

.. code-block:: sh

    docker exec -it <container_name> /bin/bash

View active containers
~~~~~~~~

.. code-block:: sh

    docker ps

Cleaning the Docker system from unnecessary data
~~~~~~~~

.. code-block:: sh

    docker system prune -f
