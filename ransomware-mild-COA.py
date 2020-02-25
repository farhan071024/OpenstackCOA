import requests
import json
import sys
import schedule 
import time 

serverids={"15ea96ba-981c-4a0c-83b6-0ebb6d7ea5cb": "web-server", "62ffe1cc-9d6d-43fc-b828-1119b5747ddb": "database-server"}

def jsoninput():
	with open(sys.argv[1]) as json_data:
		data = json.load(json_data)
	#backupdict={}
	if data["name"]=="ransomware-mild-COA":
		backups= data["backup-entities"]
		for backup in backups:
			#backuplist=[]
			#backuplist.append(str(data["number of backups"][backup]))
			#backuplist.append(str(data["backup-location"][backup]))
			#backuplist.append(str(data["backup-frequency"][backup]))
			for ids, name in serverids.iteritems():
				if (name==backup) and (data["backup-location"][backup]== "local"):
					count = int(data["number of backups"][backup])
					print createbackup(ids,name,count,data["backup-frequency"][backup])



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
                    "id": "991ff2620c0446e6b6764c173c5eb72c",
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

def createbackup(serverid,name,count,freq):
	token_id = auth()	
    #Replaces {0} from config file with the appropriate tenant id
	url2 = 'http://10.245.135.69/compute/v2.1/servers/'+serverid+'/action'

	body = {
    "createBackup": {
        "name": name+" Backup",
        "backup_type": freq,
        "rotation": count
    }
	}

	my_headers = {"X-Auth-Token": token_id}

	json_body = json.dumps(body)

	r = requests.post(url2, json_body, headers=my_headers)
	return r
    #return r.json()['server']['id']


schedule.every(2).minutes.do(jsoninput)

while True:
    schedule.run_pending()
    time.sleep(1)

