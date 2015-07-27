# ambari-custom-alerts
Custom Alerts for Ambari server

Push the new alert via Ambari REST API. 

```sh
curl -u admin:admin -i -H 'X-Requested-By: ambari' -X POST -d @alerts.json http://ambari.cloudapp.net:8080/api/v1/clusters/hdptest/alert_definitions
```
You will also need to copy the python script in /var/lib/ambari-server/resources/host_scripts and restart the ambari-server. After restart the script will be pushed in /var/lib/ambari-agent/cache/host_scripts on the different hosts.

You can find the ID of your alerts by running
```sh
curl -u admin:admin -i -H 'X-Requested-By: ambari' -X GET http://ambari.cloudapp.net:8080/api/v1/clusters/hdptest/alert_definitions
```

If we assume, that your alert is id 103. YOu can force the alert to run by
```sh
curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT  http://ambari.cloudapp.net:8080/api/v1/clusters/hdptest/alert_definitions/103?run_now=true
```
