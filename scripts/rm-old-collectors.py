# python rm-old-collectors.py <max_days> <list_or_kill_flag>

import sys
import os
import time
from sumologic import SumoLogic

#validate args, show usage if not correct
args = sys.argv
valid_args = False;
if ( len(args) == 3 ) :
	if ( (args[2] == "-k") or (args[2] == "-l") ) :
		valid_args = True;

if not valid_args :
	print ("")
	print ("Usage:")
	print ("")
	print ("  rm-old-collectors.py <max_days> <list_or_kill_flag>")
	print ("")
	print ("Examples:")
	print ("")
	print ("  List all collectors not reporting for 100+ days:")
	print ("")
	print ("     python3 rm-old-collectors.py 100 -l")
	print ("")
	print ("  Kill all collectors not reporting for 180+ days:")
	print ("")
	print ("     python3 rm-old-collectors.py 180 -k")
	sys.exit(1)

if (( "SUMO_ACCESS_ID" not in os.environ) or ("SUMO_ACCESS_KEY" not in os.environ)) :
	print ("You must have env variables defined for for SUMO_ACCESS_ID and SUMO_ACCESS_KEY")
	sys.exit(1)

# parameters are fine, real work starts here
max_days = int(args[1])
kill_flag = False;
if (args[2] == "-k") :
	kill_flag = True;

sumo = SumoLogic(os.environ['SUMO_ACCESS_ID'], os.environ['SUMO_ACCESS_KEY'])
cs = sumo.collectors("10000")
cnt = 0
now_in_ms = int(time.time()) * 1000

if kill_flag :
	print ("REMOVING OLD COLLECTORS IN 10 SECONDS. Ctrl-C if you are unsure!")
	time.sleep(10)
else :
	print ("DANGER Will Robinson. Review output before running script again with -k flag")

for c in cs:
	if (c["lastSeenAlive"] < (now_in_ms - (max_days * 86400000))) :
		date_as_string = time.strftime('%Y/%m/%d', time.gmtime(float(c["lastSeenAlive"])/1000.))
		print ("#" + str(c["id"]) + "," + date_as_string + "," + c["name"])
		if kill_flag :
			print (sumo.delete_collector(c).text)
			time.sleep(1)
		cnt+=1

print("Total old collectors processed: " + str(cnt))
