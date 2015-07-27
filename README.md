# ambari-custom-alerts
Custom Alerts for Ambari server

Push the new alert via Ambari REST API. 

```sh
curl -u admin:admin -i -H 'X-Requested-By: ambari' -X POST -d @alerts.json http://centrica01.cloudapp.net:8080/api/v1/clusters/hdptest/alert_definitions
```
You will also need to copy the python script in /var/lib/ambari-server/resources/host_scripts and restart the ambari-server
