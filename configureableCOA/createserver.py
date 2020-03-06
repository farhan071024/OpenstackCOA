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


def bootVM(url,name, image, flavor, network):
    token_id= auth()
    #Replaces {0} from config file with the appropriate tenant id
#    url2 = 'http://10.245.135.69/compute/v2.1/servers'
    url2= url	

    body = {"server": 
                {"name": name,
                # "flavorRef": "http://10.245.135.69/compute/flavors/42",
		   "flavorRef": flavor,
		 #"imageRef":"8ff221dd-89c4-4533-afd8-3b78b993f6aa",
		   "imageRef": image,
		  "networks" : [{
            		#"uuid" : "bf9b1e6c-e187-4d25-83c9-795d0ab9d065",
			"uuid" : network,
       			 }],
		  }}

    my_headers = {"X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    #return json.dumps(r.json(), indent=4)
    return r.json()['server']['id']

with open(sys.argv[1]) as json_file:
	data = json.load(json_file)
	print bootVM(data["backup"]["baseurl"],data["backup"]["server"],data["backup"]["image"],data["backup"]["flavor"],data["backup"]["network"])


