# Monitor folder for Space Quota

This alert will generate a warning if the space in your folder is above 70% of your quota and a critical if you are above 90%.

You need to modify the value of location.quota in the parameter section to match the folder that you would like to monitor.
```sh
              "name": "location.quota",
              "display_name": "Path to monitor",
              "value": "/application/digital",
```
Similarly if you want to change the threshold, modify the value for **quota.warning.threshold** and **quota.critical.threshold**.

## How to use space Quota in HDFS

The hdfs admin can create Quota. There is two types of quota: 
- space quota ( how much storage can be used )
- file quota ( how many files can be created )

This alert only check the space quota, it doesn't look into file quota.

Set a quota of 2GB on folder /application/digital - value are in bytes = 2*1024*1024*1024 = 2147483648
```sh
hdfs dfsadmin -setSpaceQuota 2147483648  /application/digital
```
NB: Quota works on raw storage

Check the quota ( can be run by any user w/ read permission on folder ) 
```sh
hdfs dfs -count -q /application/digital
       none             inf      2147483648      1832910848            1            1          104857600 /application/digital
                                    |               |
                                  Quota           Usage
```

Delete quota
```sh
hdfs dfsadmin -clrSpaceQuota /application/digital
```
