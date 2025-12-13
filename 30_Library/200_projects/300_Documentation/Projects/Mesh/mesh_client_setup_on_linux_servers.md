---
aliases: []
author:
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source: "https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/mesh-client-advanced-and-other-settings"
source_of_truth: []
status: 
tags: []
title: mesh_client_setup_on_linux_servers
type:
uid: 
updated: 
version:
---

## MESH Client Setup on Linux Servers

Installation of the MESH client on Linux servers follows exactly the same process as that detailed for a [Windows install](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-installation-guidance). The same java file installation file is used; mesh-6.2.0_20180601.jar.

To run the install start a terminal session and enter the following command;

\# java –jar mesh-6.2.0_20180601.jar 

Follow the same detailed steps as documented for the Windows install.

As with the Windows client you will need to ensure that the Keystore has been populated, that the desired log level has been set and that meshclient.cfg contains the correct file paths and login credentials for your mailbox.

Once the installation is complete and the configuration details have been input, the /MESH client can started.

1. To run the MESH client, type \# ./runMeshClient.sh &
2. To check that the Mesh client is running, type \# jobs or # ps –ef | grep mesh

If the server is rebooted, the MESH client will need to be re-started again.

The MESH client can also be set up to run as a Linux service. As a Linux service, if the server is rebooted, the client will shut down safely and automatically restart once the server is up. If the client has been started from the command line it would have to be manually restarted every time the server is rebooted.

The way services are handled on Linux depends upon the “flavour” of the Linux distribution and version. Some versions use upstart and some use systemd. For example, Ubuntu 14.04 uses upstart but has moved to systemd for version 15.04.

Below are examples of how the MESH client can be run as a service, using upstart and system; choose whichever is compatible with your system.

### Upstart Service (on Ubuntu 14.04)

Create a file in /etc/init/ called mesh.conf which will have the below format:

description "Service for the MESH Client"

author "HSCIC"

start on runlevel \[2345\]

stop on runlevel \[016\]

chdir /MESH-APP-HOME

script

./runMeshClient2.sh

end script

pre-stop script

echo 1 > ./sig/mexclient.sig

sleep 5

end script

To run the MESH client as a service, first ensure that it is not running.

\# service mesh start

To check the status

\# service mesh status

To stop the service

\# service mesh stop

The script needs to execute runMeshClient.sh but it was found that subtle changes needed to be made to the syntax to get it to work. A second version called runMeshClient2.sh was created.

#!/bin/sh

RESTART=true

while \[ "${RESTART}" = "true" \]; do

 RESTART=false

java -Dlog4j.configurationFile=./log4j2.xml -jar meshClient.jar ./meshclient.cfg

 OUTCOME=$?

\# If we get an exit code of 2 from the MESH Client, that means a restart is required.

if \[ "${OUTCOME}" = "2" \]; then

\# Apply any upgrades that have been downloaded

mv ./upgrades/meshClient-\.jar ./meshClient.jar

RESTART=true

fi

done
