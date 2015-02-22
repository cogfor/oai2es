#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

""" A library that provides a Python interface to BaasBox """

__author__ = "rene@cogfor.com"
__version__ = "0.1"

import codecs  # to manage unicode files
import json  # to manipulate JSON objects
import datetime  # to manipulate and format timestamps
import requests  # to call BaasBox APIs
import base64  # to encode the Basic Auth header

try:
    # Python >= 2.6
    import json as simplejson
except ImportError:
    try:
        # Python < 2.6
        import simplejson
    except ImportError:
        try:
            # Google App Engine
            from django.utils import simplejson
        except ImportError:
            raise ImportError, "Unable to load a json library"

BAASBOX_ADDRESS = "http://baasbox-cog4.openshift.com/"  # the BaasBox server address. NOTE: be sure to add the / at the end of the URL
BAASBOX_ADMIN_USER = "admin"  # the BaasBox user to use when a BaasBox is called
BAASBOX_ADMIN_PASSWORD = "xvbBk01b8S"  # the password to use
BAASBOX_APP_CODE = "1234567890"  # the BaasBox instance application code
BAASBOX_COLLECTION = "kennisbank"  # the BaasBox collection name

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000+000'  # BaasBox formats dates in this way

# these are the headers used to call BaasBox APIs
BASICAUTH = base64.b64encode(BAASBOX_ADMIN_USER + ":" + BAASBOX_ADMIN_PASSWORD)  # The Basic Authentication will be used
HEADERS = {u'Authorization': u"Basic " + BASICAUTH,
           u'X-BAASBOX-APPCODE': BAASBOX_APP_CODE,
           u'Content-Type': 'application/json'}


class BaasboxError(Exception):
    """ Base class for Baasbox errors """

    @property
    def message(self):
        """ Returns the first argument to construct this error."""
        return self.args[0]


class


# grants read permission on the BaasBox object to all registered users
def grantread(id):
    res = requests.put(BAASBOX_ADDRESS + "document/" + BAASBOX_COLLECTION + "/" + id + "/read/role/registered", "{}",
                       headers=HEADERS)


# inserts an object into BaasBox
# uses the collection name and BaasBox credentials defined earlier
def insertobject(json_object):
    res = requests.post(BAASBOX_ADDRESS + "document/" + BAASBOX_COLLECTION, data=json.dumps(json_object),
                        headers=HEADERS)
    if res.status_code == 200:
        # extracts the BaasBox id from the response
        baasbox_obj = json.loads(res.text)["data"]
        bb_id = baasbox_obj["id"]
        # grants permission on the object
        grantread(bb_id)
        message = json_object["_id"] + " --> " + bb_id
        print message
    else:
        error = "** Error inserting object " + json_object["_id"] + " BaasBox replied: " + res.text
        print error


# create the collection on BaasBox, if it does not exist
def createbaasboxcollection():
    res = requests.post(BAASBOX_ADDRESS + "admin/collection/" + BAASBOX_COLLECTION, "{}", headers=HEADERS)


def insert_asset(json_object):
    """ adds an asset into baasbox """






