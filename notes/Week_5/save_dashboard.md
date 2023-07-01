# Save Grafana Dashboard

With Grafana, we don't need to recreate all the panels again, but we can just access them from the dashboards.
Remember on `docker-compose.yml` we used

```
grafana:
    image: grafana/grafana
    user: "472"
    ports:
      - "3000:3000"
    volumes:
      - ./config/grafana_datasources.yaml:/etc/grafana/provisioning/datasources/datasource.yaml:ro
      - ./config/grafana_dashboards.yaml:/etc/grafana/provisioning/dashboards/dashboards.yaml:ro
      - ./dashboards:/opt/grafana/dashboards
    networks:
      - back-tier
      - front-tier
    restart: always
```

where `grafana_dashboards.yaml` is a configuration file used to set up Grafana dashboards for monitoring machine learning models. The dashboards are stored in the specified path and Grafana scans for changes at the specified interval. The configuration also allows for the creation of folders in Grafana based on the file structure

```
apiVersion: 1

providers:
  # <string> an unique provider name. Required
  - name: 'Evidently Dashboards'
    # <int> Org id. Default to 1
    orgId: 1
    # <string> name of the dashboard folder.
    folder: ''
    # <string> folder UID. will be automatically generated if not specified
    folderUid: ''
    # <string> provider type. Default to 'file'
    type: file
    # <bool> disable dashboard deletion
    disableDeletion: false
    # <int> how often Grafana will scan for changed dashboards
    updateIntervalSeconds: 10
    # <bool> allow updating provisioned dashboards from the UI
    allowUiUpdates: false
    options:
      # <string, required> path to dashboard files on disk. Required when using the 'file' type
      path: /opt/grafana/dashboards
      # <bool> use folder names from filesystem to create folders in Grafana
      foldersFromFilesStructure: true
```

Also make sure you have the Grafana dashboard configuration file `dashboards/data_drift.json`.


[Previous](data_quality.md) | [Next](debugging.md)