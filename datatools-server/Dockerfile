FROM openjdk:8-jdk

ENV VERSION=dev


## Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends maven git && \
    apt-get clean /////////&& \
    rm -rf /var/lib/apt/lists/*

#RUN mvn -v

RUN git clone -b dev https://github.com/ibi-group/datatools-server.git /opt/datatools-server
WORKDIR /opt/datatools-server

RUN mvn dependency:go-offline

VOLUME /root/.m2

ADD ./config/*.yml /config/

COPY /config/env-server.yml /opt/datatools-server/configurations/default/env.yml
COPY /config/server.yml /opt/datatools-server/configurations/default/server.yml
COPY /config/go-europa.pem /opt/datatools-server/configurations/default/go-europa.pem
COPY /config/awsconfig /root/.aws/config
RUN mvn package -Dmaven.test.skip=true


EXPOSE 4000

CMD java -jar target/dt-v3.2.0-1048-g47371e0.jar  /opt/datatools-server/configurations/default/env.yml /opt/datatools-server/configurations/default/server.yml
