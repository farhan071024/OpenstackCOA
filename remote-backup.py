import requests
import json
import sys
import schedule 
import time 
from paramiko import SSHClient
from scp import SCPClient
import subprocess

checksums={"web-server Backup2": "baa372b8cd200efd1b20fcaf5177932f"}

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
			return downloadimage(sc["id"],sc["name"])

def downloadimage(image,name):
	token_id= auth()
	url='http://10.245.135.69/image/v2/images/'+image+'/file'	
	my_headers = {"X-Auth-Token": token_id}
	r = requests.get(url,headers=my_headers)
	if r.headers["Content-MD5"]== checksums[name]:
		file = open("image.raw", "wb")
		file.write(r.content)
		file.close()
		return "Image downloaded!"
	else:
		return  "Intergrity check failed!"




def scp2():
	subprocess.Popen(["scp", "image.raw", "ubuntu@10.245.135.69:/home/ubuntu/openstackcoa"])
	print "done"
	return 
#print getimage("web-server Backup2")
scp2()

