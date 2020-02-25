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


def listports(token):
	url='http://10.245.135.69:9696/v2.0/security-group-rules'	
	my_headers = {"X-Auth-Token": token}
	r = requests.get(url,headers=my_headers)
	return json.dumps(r.json())
	#return r

def createsecuritygrouprule(token):
	url='http://10.245.135.69/compute/v2.1/os-security-group-rules'	
	my_headers = {"X-Auth-Token": token}
	body=    { "security_group_rule": {
        "parent_group_id": "022f0c2b-d1fa-4929-b49d-77facf1e217a",
        "ip_protocol": "tcp",
        "from_port": 22,
        "to_port": 22,
        "cidr": "10.0.0.0/24"
    }
}
	json_body = json.dumps(body)
	r = requests.post(url,json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers

token_id= auth()
print createsecuritygrouprule(token_id)
