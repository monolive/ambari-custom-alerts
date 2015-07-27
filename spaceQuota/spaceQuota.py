#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# Generate an alert in Ambari when going pass threshold
#
# Olivier Renault <orenault@hortonworks.com>
# 

import urllib2
#import ambari_simplejson as json # simplejson is much faster comparing to Python 2.6 json module and has the same functions set.
import json
import logging

from resource_management.libraries.functions.curl_krb_request import curl_krb_request
from resource_management.core.environment import Environment

LABEL = 'the current value is {c}%, the threshold is {t}%'
NN_HTTP_ADDRESS_KEY = '{{hdfs-site/dfs.namenode.http-address}}'
#NN_HTTPS_ADDRESS_KEY = '{{hdfs-site/dfs.namenode.https-address}}'
#NN_HTTP_POLICY_KEY = '{{hdfs-site/dfs.http.policy}}'

#KERBEROS_KEYTAB = '{{hdfs-site/dfs.web.authentication.kerberos.keytab}}'
#KERBEROS_PRINCIPAL = '{{hdfs-site/dfs.web.authentication.kerberos.principal}}'
#SECURITY_ENABLED_KEY = '{{cluster-env/security_enabled}}'
#SMOKEUSER_KEY = "{{cluster-env/smokeuser}}"

LOCATION_QUOTA = 'location.quota'
QUOTA_WARN = 'quota.warning.threshold'
QUOTA_CRIT = 'quota.critical.threshold'


logger = logging.getLogger()

def get_tokens():
  """
  Returns a tuple of tokens in the format {{site/property}} that will be used
  to build the dictionary passed into execute
  """
  return (NN_HTTP_ADDRESS_KEY, LOCATION_QUOTA, QUOTA_WARN, QUOTA_CRIT)

#  return (NN_HTTP_ADDRESS_KEY, NN_HTTPS_ADDRESS_KEY, NN_HTTP_POLICY_KEY, KERBEROS_KEYTAB, KERBEROS_PRINCIPAL, 
#  	SECURITY_ENABLED_KEY, SMOKEUSER_KEY, LOCATION_QUOTA, QUOTA_WARN, QUOTA_CRIT)

def execute(configurations={}, parameters={}, host_name=None):
  """
  Returns a tuple containing the result code and a pre-formatted result label

  Keyword arguments:
  configurations (dictionary): a mapping of configuration key to value
  parameters (dictionary): a mapping of script parameter key to value
  host_name (string): the name of this host where the alert is running
  """

  if configurations is None:
    return (('UNKNOWN', ['There were no configurations supplied to the script.']))
  
  if NN_HTTP_ADDRESS_KEY in configurations:
    http_uri = configurations[NN_HTTP_ADDRESS_KEY]

  if LOCATION_QUOTA in parameters:
    location_quota = parameters[LOCATION_QUOTA]

  if QUOTA_WARN in parameters:
    quota_warn = parameters[QUOTA_WARN]
    
  if QUOTA_CRIT in parameters:
    quota_crit = parameters[QUOTA_CRIT]

  # start out assuming an OK status
  label = None
  result_code = "OK"

  url = "http://" + http_uri + "/webhdfs/v1" + location_quota + "?op=GETCONTENTSUMMARY"

  try:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    result = json.loads(response.read())
    result_in_percent = int(float(result["ContentSummary"]["spaceConsumed"])/float(result["ContentSummary"]["spaceQuota"])*100)
    if ( result_in_percent >= int(quota_crit)):
      result_code = 'CRITICAL'
      label = LABEL.format(c=result_in_percent, t=quota_crit)
    elif (result_in_percent >= int(quota_warn)):
      result_code = 'WARNING'
      label = LABEL.format(c=result_in_percent, t=quota_warn)
    else:
      result_code = "OK"
      label = "The current value is {c}%".format(c=result_in_percent)

  except Exception, e:
    label = str(e)
    result_code = 'UNKNOWN'

  return ((result_code, [label]))