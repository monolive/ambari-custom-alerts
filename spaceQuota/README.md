# Monitor folder for Space Quota

This alert will generate a warning if the space in your folder is above 70% of your quota and a critical if you are above 90%.

You need to modify the value of location.quota in the parameter section to match the folder that you would like to monitor.
```sh
              "name": "location.quota",
              "display_name": "Path to monitor",
              "value": "/application/digital",
```
If you want to change the threshold, modify the value of quota.warning.threshold and quota.critical.threshold.
