import codecs  # to manage unicode files
import json  # to manipulate JSON objects
import datetime  # to manipulate and format timestamps
import requests  # to call BaasBox APIs
import base64  # to encode the Basic Auth header

baasbox_address = "http://localhost:9000/"  # the BaasBox server address. NOTE: be sure to add the / at the end of the URL
baasbox_admin_user = "admin"		# the BaasBox user to use when a BaasBox is called
baasbox_admin_password = "admin"  # the password to use
baasbox_app_code = "1234567890"		# the BaasBox instance application code
baasbox_collection = "document"

#these are the headers used to call BaasBox APIs
basicauth = base64.b64encode(baasbox_admin_user + ":" + baasbox_admin_password)  # The Basic Authentication will be used
headers = {u'Authorization':u"Basic " + basicauth,
           u'X-BAASBOX-APPCODE':baasbox_app_code,
           u'Content-Type':'application/json'}


def add_asset(json_object):
    headers = {u'X-BB-SESSION':'2d04a009-9ceb-4a90-a5e1-e021951ca790'}
    payload = {'name': 'test',
               'meta': '{"pizzaname": "Margherita", "price": 5}'}
    res = requests.post(baasbox_address + "admin/asset", data=payload, headers=headers)
    print res.text

    if res.status_code == 200:
        baasbox_obj = json.loads(res.text)["data"]
        print baasbox_obj


def auth(username='admin', password='admin', appcode='1234567890'):
    payload = {'username': username,
                'password': password,
                'appcode' :appcode}
    res = requests.post(baasbox_address + "login", data=payload)
    return json.loads(res.text)['data']['X-BB-SESSION']

#inserts an object into BaasBox
#uses the collection name and BaasBox credentials defined earlier
def insertobject(json_object):
    res = requests.post(baasbox_address + "document/" + baasbox_collection, data=json.dumps(json_object),
                        headers=headers)
    if (res.status_code == 200):
        #extracts the BaasBox id from the response
        baasbox_obj = json.loads(res.text)["data"]
        bb_id = baasbox_obj["id"]
        #grants permission on the object
        #grantread(bb_id)
        message = json_object["_id"] + " --> " + bb_id
        print message
    else:
        error = "** Error inserting object " + json_object["_id"] + " BaasBox replied: " + res.text
        print error

json_object = 'name=margherita&meta={"pizzaname": "Margherita", "price": 5}'
#res = auth()
add_asset(json_object)

