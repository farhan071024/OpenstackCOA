import requests
import json


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
	#print r.headers
	#print r.headers.get('X-Subject-Token')
	#print json.dumps(r.json())
	
	token_id = r.headers.get('X-Subject-Token')
	return token_id

def firewall(token):
	url='http://10.245.135.69:9696/v2.0/fwaas/firewall_rules'	
	my_headers = {"X-Auth-Token": token}
	r = requests.get(url,headers=my_headers)
	print json.dumps(r.json())

def createfirewallrule(token):
	url='http://10.245.135.69:9696/v2.0/fwaas/firewall_rules'	
	my_headers = {"X-Auth-Token": token}
	body=   { "firewall_rule": {
        "action": "allow",
	"destination_ip_address":"10.245.135.69",
        "destination_port": "80",
	"name": "firewall-rule-1",
        "name": "ALLOW_HTTP",
        "protocol": "tcp",
	"source_ip_address": "10.245.135.51",
	"source_port": "80"
    }
}
	json_body = json.dumps(body)
	r = requests.post(url,data=json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers

def createsecuritygroup(token):
	url='http://10.245.135.69:9696/v2.0/security-groups'	
	my_headers = {"X-Auth-Token": token}
	body= {
    "security_group": {
        "name": "new-webservers",
        "description": "security group for webservers"
    }
}
	#print token
	json_body = json.dumps(body)
	r = requests.post(url,json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers

def createsecuritygrouprule(token):
	url='http://10.245.135.69:9696/v2.0/security-group-rules'	
	my_headers = {"X-Auth-Token": token}
	body= {
    "security_group": {
        "name": "new-webservers",
        "description": "security group for webservers",
        "stateful": True
    }
}
	print token
	json_body = json.dumps(body)
	r = requests.post(url,json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers

def createports(token):
	url='http://10.245.135.69:9696/v2.0/ports'	
	my_headers = {"X-Auth-Token": token}
	body= {
    "port": {
        "name": "private-port",
        "network_id": "bf9b1e6c-e187-4d25-83c9-795d0ab9d065",
        "allowed_address_pairs": [
            {
                "ip_address": "12.12.11.12",
                "mac_address": "fa:14:2a:b3:cb:f0"
            },
		{
                "ip_address": "12.12.11.23",
                "mac_address": "fa:14:2a:b4:cb:f0"
            }
        ]
        
    }
}
	print token
	json_body = json.dumps(body)
	r = requests.post(url,json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers

def updateports(token):
	url='http://10.245.135.69:9696/v2.0/ports/b9b65a1b-5d01-4ade-be2a-9014b59aa4e1'	
	my_headers = {"X-Auth-Token": token}
	body= {
    "port": {
        "device_id": "d90a13da-be41-461f-9f99-1dbcf438fdf2",
        "device_owner": "compute:nova",
        "name": "test-for-port-update",
	"allowed_address_pairs": [
            {
                "ip_address": "132.142.121.12",
                
            }
        ]
        
    }
}
	#print token
	json_body = json.dumps(body)
	r = requests.put(url,json_body,headers=my_headers)
	print json.dumps(r.json())
	#print r.headers


if __name__ == "__main__":
	token_id = auth()
	#createfirewallrule(token_id)	
	#createsecuritygroup(token_id)
	#firewall(token_id)
	#createports(token_id)
	updateports(token_id)

	
	
