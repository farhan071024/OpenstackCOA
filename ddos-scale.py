import requests
import json
import sys
import schedule 
import time 


#ddosscaleCOA=["scale-entitites", "scale-size","scale-duration"]
ports={"database-server": "5000", "web-server": "6020"}
serverids={}

def jsoninput():
	with open(sys.argv[1]) as json_data:
		data = json.load(json_data)
	scaledict={}
	if data["name"]=="ddos-scale-COA":
		servers=data["scale-entitites"]
		for server in servers:
			scaleinfo=[str(data["scale-size"][server]),str(data["scale-duration"][server])]
			scaledict[str(server)]= scaleinfo			
	
	for key in scaledict.keys():
		scalemain(str(key),str(scaledict[key][0]),str(scaledict[key][1]))
	print serverids	
	return "done"

def scalemain(name,count,duration):
	token_id = auth()
	count= int(count)
	while count>0:
		testname=name+str(count)
		serverid=bootVM(token_id,testname)
		serverids[str(serverid)]=str(duration)		
		count=count-1	
	return		

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

def bootVM(token_id, name):
    #Replaces {0} from config file with the appropriate tenant id
    url2 = 'http://10.245.135.69/compute/v2.1/servers'

    body = {"server": 
                {"name": name,
                 "flavorRef": "http://10.245.135.69/compute/flavors/42",
		 "imageRef":"8ff221dd-89c4-4533-afd8-3b78b993f6aa",
		  "networks" : [{
            		"uuid" : "bf9b1e6c-e187-4d25-83c9-795d0ab9d065",
       			 }],
		  }}

    my_headers = {"X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    #return json.dumps(r.json(), indent=4)
    return r.json()['server']['id']

def listflavors(token):
	url='http://10.245.135.69/compute/v2.1/servers'	
	my_headers = {"X-Auth-Token": token}
	r = requests.get(url,headers=my_headers)
	return json.dumps(r.json())

def deletevms(serverid):
	token_id= auth()
	url='http://10.245.135.69/compute/v2.1/servers/'+serverid	
	my_headers = {"X-Auth-Token": token_id}
	r = requests.delete(url,headers=my_headers)
	
	


jsoninput()
if len(serverids)>0:
	for ids in serverids.keys():
		schedule.every(int(serverids[ids])).seconds.do(deletevms,str(ids))
while True:
    schedule.run_pending()
    time.sleep(1)
	



