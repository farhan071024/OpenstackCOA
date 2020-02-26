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


def deleterule(ruleid):
	token_id= auth()
	url='http://10.245.135.69/compute/v2.1/os-security-group-rules/'+ruleid	
	my_headers = {"X-Auth-Token": token_id}
	r = requests.delete(url,headers=my_headers)
	return r


def createsecuritygrouprule(groupid,ips):
	token_id= auth()
	url='http://10.245.135.69/compute/v2.1/os-security-group-rules'	
	my_headers = {"X-Auth-Token": token_id}
	body=    { "security_group_rule": {
        "parent_group_id": groupid,
        "ip_protocol": "tcp",
        "from_port": 22,
        "to_port": 22,
        "cidr": ips
    }
}
	json_body = json.dumps(body)
	r = requests.post(url,json_body,headers=my_headers)
	print json.dumps(r.json())

def listsecuritygroups(name):
	token_id= auth()
	url='http://10.245.135.69/compute/v2.1/os-security-groups'	
	my_headers = {"X-Auth-Token": token_id}
	
	r = requests.get(url,headers=my_headers)
	data= json.dumps(r.json())
	data=json.loads(data)
	#print data["security_groups"]
	for sc in data["security_groups"]:
		print sc["name"]
		if sc["name"]== name:
			ruleids=[]
			for sc2 in sc["rules"]:
				#print sc2["id"]
				ruleids.append(sc2["id"])
			return ruleids, sc["id"]
		


def jsoninput():
	with open(sys.argv[1]) as json_data:
		data = json.load(json_data)
		#print(data)
	if data["name"]=="securitygroup-rule-maintenance-COA":
		servers=data["servers"]
		for server in servers:
			schedule.every(int(data["securitygroup-rule-scan-frquency"][server])).seconds.do(securitygroupmain,server,data["allowed-ips-cidr"][server])
		while True:
			schedule.run_pending()
			time.sleep(1)	
			

def securitygroupmain(server, allowed_ips):
	ruleids,groupid=listsecuritygroups(server)
	for ids in ruleids:
		print deleterule(ids)
	print "deleted security rules..."
	for ips in allowed_ips:
		createsecuritygrouprule(groupid,ips)
	print "created new security rules"

			

jsoninput()
