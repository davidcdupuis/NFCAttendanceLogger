#!usr/bin/python

import MySQLdb

db = MySQLdb.connect("localhost", "monitor", "1234", "AttendanceDB")

curs=db.cursor()

sql = "SELECT * FROM CLASS WHERE tdate = '2015-04-16' AND '15:30:50' >= stime AND etime >= '15:30:50'"

try:
	curs.execute(sql)
	results = curs.fetchall()
	for row in results:
		id = row[0]
		name = row[1]
		date = row[2]
		sTime = row[3]
		eTime = row[4]
		print "id = %d, nom = %s, date = %s, startTime = %s, endTime = %s " % (id, name,date,sTime,eTime)

except:
	print "unable to fetch classes"

print "\n\n"


db.close()
