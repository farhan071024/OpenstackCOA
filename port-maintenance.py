import requests
import json
import sys
import schedule 
import time 


#portMaintenanceCOA=["app-port-scan","app-port-scan-frequency","last-app-port-modification-count"]
ports={"database-server": "5000", "web-server": "6020"}

def jsoninput():
	with open(sys.argv[1]) as json_data:
		data = json.load(json_data)
		#print(data)
	if data["name"]=="port-maintenance-COA":
		#print (returnports (data["app-port-scan"],data["app-port-scan-frequency"],ports))
		return returnports (data["app-port-scan"],data["app-port-scan-frequency"],ports)


def returnports(data,data2,ports):
	portnums={}
	for port in data and data2.keys():
		portnums[ports[port]] = data2[port]
	return portnums

################################################################ OpenStack ###########################################################
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
	url='http://10.245.135.69:9696/v2.0/ports'	
	my_headers = {"X-Auth-Token": token}
	r = requests.get(url,headers=my_headers)
	return json.dumps(r.json())

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

def updateports(token,port_id, ip_address):
	url='http://10.245.135.69:9696/v2.0/ports/'+port_id	
	my_headers = {"X-Auth-Token": token}
	body= {
    "port": {
        
	"allowed_address_pairs": [
            {
                "ip_address": ip_address,
                
            }
        ]
        
    }
}
	json_body = json.dumps(body)
	r = requests.put(url,json_body,headers=my_headers)
	print json.dumps(r.json())

def portscanmain(token_id):
	portlist=jsoninput()
	#portnums= list(portlist,keys())
	data=listports(token_id)
	data=json.loads(data)
	newportlist={}
	for port in portlist.keys():
		for item in data["ports"]:
			if item["name"]== port:
				portid=item["id"]
				itemlist= [str(portlist[port]),str(portid)]
				newportlist[port]=itemlist
						
	return newportlist
				


#if __name__ == "__main__":
token_id = auth()
portinfo= portscanmain(token_id)
for portid in portinfo.values():
	schedule.every(int(portid[0])).seconds.do(updateports,token_id,portid[1],"200.142.121.12")
while True:
    schedule.run_pending()
    time.sleep(1)
	

	
	
