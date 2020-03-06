import json
import sys

def createCOA(argv):
	param=[]
	for x in argv[2:]:
		param.append(x)
	
	data={argv[1]:param}
	with open(argv[1]+'.json', 'w') as f:
    		json.dump(data, f)
	return "json created"

print createCOA(sys.argv)
	
