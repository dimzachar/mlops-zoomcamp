# Docker Compose File

A Docker Compose file is used to define and manage a multi-container Docker application. It's a YAML file that contains all the necessary configurations to run the application. The services defined in this file are typically used in a development environment for testing or in a production environment for deployment.

## Step 5: Create a Docker Compose File

In your project directory, create a file named `docker-compose.yml`

```bash
touch docker-compose.yml
```

## Step 6: Configure Docker Compose

Next, we'll configure the Docker Compose file, including the specification of volumes for Grafana.
We'll add a PostgreSQL database, an Adminer for managing the database content, and Grafana for dashboarding.

Here's an example of `docker-compose.yml`:

```
# Specifies the Docker Compose file version
version: '3.7'

# Declares volumes that can be used by services in the Docker Compose file
volumes: 
  # Declares a volume named grafana_data
  grafana_data: {}

# Defines networks that can be used by services in the Docker Compose file
networks:
  # Declares a network named front-tier
  front-tier:
  # Declares a network named back-tier
  back-tier:

# Defines the services that make up your app
services:
  # Defines a service named db
  db:
    # Specifies the Docker image to use for this service
    image: postgres
    # Ensures that the service is always restarted if it stops
    restart: always
    # Sets environment variables for the service
    environment:
      # Sets the password for the Postgres database
      POSTGRES_PASSWORD: example
    # Maps ports between the host and the container
    ports:
      - "5432:5432"
    # Specifies the networks that this service is part of
    networks:
      - back-tier

  # Defines a service named adminer
  adminer:
    image: adminer
    restart: always
    ports:
      - "8080:8080"
    networks:
      - back-tier
      - front-tier  

  # Defines a service named grafana
  grafana:
    image: grafana/grafana
    # Sets the user ID under which the service will run
    user: "472"
    ports:
      - "3000:3000"
    # Maps local directories or files to directories inside the container
    volumes:
      # Maps a local file to a file inside the container, and makes it read-only
      - ./config/grafana_datasources.yaml:/etc/grafana/provisioning/datasources/datasource.yaml:ro
      - ./config/grafana_dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml:ro
      - ./dashboards:/opt/grafana/dashboards
    networks:
      - back-tier
      - front-tier
    restart: always
```

The Docker Compose file does the following:

- Postgres Database (db service): It sets up a Postgres database service using the official Postgres Docker image. The database is accessible on port 5432 and is connected to the back-tier network. The password for the database is set as an environment variable.

- Adminer (adminer service): Adminer is a full-featured database management tool available for MySQL, PostgreSQL, SQLite, MS SQL, Oracle, Firebird, SimpleDB, Elasticsearch, and MongoDB. In this case, it's used as a web interface for managing the Postgres database. It uses the official Adminer Docker image and is accessible on port 8080. It's connected to both the back-tier and front-tier networks.

- Grafana (grafana service): Grafana is an open-source platform for monitoring and observability. It allows you to query, visualize, alert on, and understand your metrics no matter where they are stored. In this case, it's set up using the official Grafana Docker image and is accessible on port 3000. It's connected to both the back-tier and front-tier networks. The service uses a specific user ID to run and mounts several volumes for configuration and dashboards.

- The restart: always directive for each service ensures that if a service goes down for any reason, Docker will automatically attempt to restart it.

- The volumes and networks at the top of the file are declared but not used in this specific file. They can be used by other services that are not defined in this file but are part of the same Docker environment.

This Docker Compose file is typically used in a scenario where you want to set up a monitoring system for your application. The Postgres database would store your application data, Adminer would provide a web interface for managing the database, and Grafana would be used to create visualizations and dashboards based on the data in the database.

## Step 8: Create Grafana Data Source Configuration

We'll create a Grafana data source configuration file. It's used to define the data sources that Grafana should connect to. A data source in Grafana represents a back-end database, such as PostgreSQL, MySQL, InfluxDB, or a myriad of other data storage systems.
In your project directory, create a new directory named `config` and a file within it named `grafana_datasources.yaml`:

```
mkdir config
touch config/grafana_datasources.yaml
```

and specify it as:

```
# Specifies the version used in this configuration file
apiVersion: 1

# Defines the data sources that Grafana should connect to
datasources:
  # Defines a data source
  - 
    # Specifies the name of the data source
    name: PostgreSQL
    # Specifies the type of the data source
    type: postgres
    # Specifies how Grafana should access the data source
    # The 'proxy' mode means that all requests are proxied via the Grafana backend/server
    access: proxy
    # Specifies the URL (including the port number) of the data source
    url: db.:5432
    # Specifies the name of the database that Grafana should connect to
    database: test
    # Specifies the username that Grafana should use to connect to the database
    user: postgres
    # Specifies secure data like passwords
    secureJsonData:
      # Sets the password for the database connection
      password: 'example'
    # Specifies additional JSON data for the data source configuration
    jsonData:
      # Disables SSL mode for the database connection
      sslmode: 'disable'
```

In this file, a single data source is defined:

- **PostgreSQL:** A PostgreSQL database is set up as a data source. The configuration specifies that Grafana should connect to a service named `db` on port 5432, using the database named `test`. The connection is made using the username `postgres` and the password `example`. The connection is made in `proxy` mode, meaning that all requests from the Grafana server are proxied via the Grafana backend/server, and Grafana adds CORS headers and authorization. SSL mode is disabled for this connection.

This configuration file is used in the context of the Docker Compose setup we provided earlier. The Grafana service in the Docker Compose file uses this configuration file to set up its connection to the PostgreSQL database. The file would be placed in the `./config` directory relative to the Docker Compose file, and it's mounted into the Grafana container at the `/etc/grafana/provisioning/datasources/datasource.yaml` path.

This setup allows Grafana to pull data from the PostgreSQL database, which it can then use to create visualizations and dashboards. This is particularly useful in a monitoring setup, where you might want to visualize metrics from your application that are stored in the PostgreSQL database.


## Step 9: Build and Run Docker Compose

Finally, we'll build and run our Docker Compose configuration. In your terminal, navigate to the directory containing `docker-compose.yml` and run:

```bash
docker-compose up --build
```

You should see that all your containers are successfully created. You can verify this by accessing Grafana and Adminer through your browser at `localhost:3000` and `localhost:8080`, respectively.

That's it! You've now set up an environment for MLOps using Docker Compose. In the next part, we'll load some data and start implementing monitoring for our service. Stay tuned!

[Previous](setup_env.md) | [Next](baseline.md)