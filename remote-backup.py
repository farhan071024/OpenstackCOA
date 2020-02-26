import requests
import json
import sys
import schedule 
import time 


def auth():
	url = 'http://10.245.135.69/identity/v3/auth/tokens'
    
	body=   {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "id": "991ff2620c0446e6b6764c173c5eb72c ",
                    "password": "password"
                }
            }
        },
        "scope": {
            "project": {
                "domain": {
                    "id": "default"
                },
                "name": "admin"
            }
        }
    }
}
                      
	json_body = json.dumps(body)
	r = requests.post(url, json_body)
		
	token_id = r.headers.get('X-Subject-Token')
	return token_id

def getimage(name):
	token_id= auth()
	url='http://10.245.135.69/image/v2/images'	
	my_headers = {"X-Auth-Token": token_id}
	r = requests.get(url,headers=my_headers)
	data=json.dumps(r.json())
	data=json.loads(data)
	for sc in data["images"]:
		if sc["name"]== name:			
			return downloadimage(sc["id"])

def downloadimage(image):
	token_id= auth()
	url='http://10.245.135.69/image/v2/images/'+image+'/file'	
	my_headers = {"X-Auth-Token": token_id}
	r = requests.get(url,headers=my_headers)
	return r

print getimage("web-server Backup2")
