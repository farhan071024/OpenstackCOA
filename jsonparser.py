#!/usr/bin/env python
import json
import sys
import schedule 
import time 

portMaintenanceCOA=["app-port-scan","app-port-scan-frequency","last-app-port-modification-count"]
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


#if __name__ == "__main__":
schedule.every(1).minutes.do(jsoninput)
while True:
    schedule.run_pending()
    time.sleep(1)
