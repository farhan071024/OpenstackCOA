import json
import sys


with open(sys.argv[2]+'.json') as json_file:
	data = json.load(json_file)
	if ((len(sys.argv)-3) == len(data[sys.argv[2]])):
		print "semantic matched"
		i=0
		data2={}
		for x in sys.argv[3:]:
			data2[str(data[sys.argv[2]][i])]=x
			i=i+1
		with open(sys.argv[1]+'.json') as json_file:
			data3 = json.load(json_file)
			data3[str(sys.argv[2])]=data2
			print data3
		with open(sys.argv[1]+'.json', 'w') as f:
    			json.dump(data3, f)
			print "successful"			
	else:
		print  "doesnot match"


	
