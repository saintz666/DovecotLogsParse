from time import sleep, time
import cPickle
import csv
import math

session_holder={}
session_data=[]

import os
starttime=time()



def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])

for file in os.listdir(os.getcwd()):
	if file.startswith("2017"):
		print "Parsing %s" % (file)
		with open(os.path.join(os.getcwd(), file)) as line:
			for lines in line:
				session_data=[]
				try:
					if ("pop3-login:" in lines) or ("imap-login:" in lines):
						if ("46.214.45.232" in lines) or ("176.37.68.78" in lines) or ("202.65.32.175" in lines) or ("110.173.190.68" in lines) or ("92.239.233.75" in lines):
							temp_sessions = lines.split(',')[3].split("=")[1]
							temp_rip = lines.split(',')[4].split("=")[1]
							if temp_sessions not in session_holder:
								session_data.append([temp_sessions,temp_rip]) 
								session_holder[temp_sessions] = session_data
							else:
								continue
					
					elif (": user" in lines) and ("out=" in lines) and ("session=" in lines):
						temp_sessions=""
						if "session=" in lines.split(',')[4]:
							temp_sessions = lines.split(',')[4].split('=')[1]
							param_01 = lines.split(',')[5].split('=')[1]
							param_02 = lines.split(',')[6].split('=')[1]
							param_03 = lines.split(',')[7].split('=')[1]
							param_04 = lines.split(',')[8].split('=')[1]
							param_05 = lines.split(',')[9].split('=')[1]

						elif "session=" in lines.split(',')[5]:
							temp_sessions = lines.split(',')[5].split('=')[1]
							param_01 = lines.split(',')[6].split('=')[1]
							param_02 = lines.split(',')[7].split('=')[1]
							param_03 = lines.split(',')[8].split('=')[1]
							param_04 = lines.split(',')[9].split('=')[1]
							param_05 = lines.split(',')[10].split('=')[1]
							pass
						elif "session=" in lines.split(',')[6]:
							temp_sessions = lines.split(',')[6].split('=')[1]
							param_01 = lines.split(',')[7].split('=')[1]
							param_02 = lines.split(',')[8].split('=')[1]
							param_03 = lines.split(',')[9].split('=')[1]
							param_04 = lines.split(',')[10].split('=')[1]
							param_05 = lines.split(',')[11].split('=')[1]

						elif "session=" in lines.split(',')[7]:
							temp_sessions = lines.split(',')[7].split('=')[1]
							param_01 = lines.split(',')[8].split('=')[1]
							param_02 = lines.split(',')[9].split('=')[1]
							param_03 = lines.split(',')[10].split('=')[1]
							param_04 = lines.split(',')[11].split('=')[1]
							param_05 = lines.split(',')[12].split('=')[1]

						elif "session=" in lines.split(',')[8]:
							temp_sessions = lines.split(',')[8].split('=')[1]
							param_01 = lines.split(',')[9].split('=')[1]
							param_02 = lines.split(',')[10].split('=')[1]
							param_03 = lines.split(',')[11].split('=')[1]
							param_04 = lines.split(',')[12].split('=')[1]
							param_05 = lines.split(',')[13].split('=')[1]
						else:
							print lines

						if temp_sessions in session_holder:
							if "/" in param_05:
								temp_type = "POP"
							else:
								temp_type = "IMAP"
							session_holder[temp_sessions].append([temp_type,param_01,param_02,param_03,param_04,param_05.replace("\n","")])
				except Exception, err:
					print "[ERROR] with line - %s" % lines

#for key in session_holder:
#	if len(session_holder[key]) != 2:
#		print session_holder[key]

bytes_in_imap = 0
bytes_out_imap =0
bytes_in_pop = 0
bytes_out_pop = 0
error_count = 0

for key in session_holder:
	if len(session_holder[key]) == 2:
		if session_holder[key][1][0] == "IMAP":
			bytes_in_imap += int(session_holder[key][1][1])
			bytes_out_imap += int(session_holder[key][1][2])
		elif session_holder[key][1][0] == "POP":
			bytes_in_pop += int(session_holder[key][1][1])
			bytes_out_pop += int(session_holder[key][1][2])
	else:
		error_count += 1


with open('dovecot_results.csv', 'wb') as outcsv:   
    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerow(['Session', 'IP', 'Type', 'Param 01', 'Param 02', 'Param 03', 'Param 04', 'Param 05'])
    for key in session_holder:
    	if len(session_holder[key]) == 2:
        	writer.writerow([session_holder[key][0][0], session_holder[key][0][1], session_holder[key][1][0], session_holder[key][1][1], session_holder[key][1][2], session_holder[key][1][3], session_holder[key][1][4], session_holder[key][1][5]])


FILE = open("dovecot_parse.dat", 'wb')
cPickle.dump(session_holder, FILE)
FILE.close()

print "\nParse Completed - %s \n\n" % (time()-starttime)
print "Session Without Data:%s/%s\nIMAP Bytes IN:%s\nIMAP Bytes OUT:%s\nPOP Bytes IN:%s\nPOP Bytes OUT:%s" % (error_count,len(session_holder),convert_size(bytes_in_imap),convert_size(bytes_out_imap),convert_size(bytes_in_pop),convert_size(bytes_out_pop))