#########################################################################################################################
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
##############################################################################################################################################
