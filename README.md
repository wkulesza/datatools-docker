Datatools GTFS Editor

This repo contains goEuropa Dockerfiles of Conveyal Data Tools for Quick and easy GTFS editing, which is composed of two parts:

    a backend
    a UI

The modifications include:
- usage of own graphhopper
- ports changed

git clone https://github.com/wkulesza/datatools-docker.git
cd datatools_docker
cp ./datatools-server/config/env-server.yml.tmp ./datatools-server/config/env-server.yml
cp ./datatools-server/config/server.yml.tmp ./datatools-server/config/server.yml
cp ./datatools-ui/config/env-client.yml.tmp ./datatools-ui/config/env-client.yml
cp ./datatools-ui/config/settings-client2.yml.tmp ./datatools-ui/config/settings-client2.yml


Edit the configuration files and view https://data-tools-docs.ibi-transit.com/en/latest/dev/deployment/ for documentation:

docker-compose up -d 

Then navigate to http://localhost:9081