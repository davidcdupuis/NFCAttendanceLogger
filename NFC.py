#!usr/bin/python
import MySQLdb, datetime, shlex, subprocess, re, time

db = MySQLdb.connect("localhost","monitor","1234","AttendanceDB")
curs = db.cursor()

output = subprocess.check_output(["nfc-list"])
output = output.decode("utf8")

uid = re.search(r'((\w){2}\s\s){4}',output).group(0).strip().split("  ")
uid = ' '.join(uid).upper()

print ("\n\nUID is: ")
print (uid)

#verifier si l'utilisateur est dans la base
sql = "SELECT * FROM USER WHERE USER.uid = '%s'" % (uid)

try:
	curs.execute(sql)
	result = curs.fetchone()
except:
	print "unable to get info from DB"


if result is None:
	print("UID non existant, would you like to add user?")

	name = raw_input("Please enter your name: ")
	lastname = raw_input("Please enter your surname: ")
	s = "Thank you, your name is: %s, your surname is %s" % (name,lastname)
	print(s)

	sql = "INSERT INTO USER (uid,name,surname) VALUES ('%s','%s','%s')" % (uid,name,lastname)

	try:
		curs.execute(sql)
		db.commit()
	except:
		print "Unable to add user to DB"
		db.rollback()

	sql2 = "SELECT * FROM USER"

	try:
		curs.execute(sql2)
		results = curs.fetchall()
		for row in results:
			id = row[0]
			uid = row[1]
			name = row[2]
			surname = row[3]
			print "id = %d, uid = %s, name = %s, surname = %s" % (id, uid, name, surname)

	except:
		print "Unable to get user array"


userId = result[0]
userUID = result[1]
userName = result[2]
userSurname = result[3]
print "\n\nYour info: id = %d, uid = %s, name = %s, surname = %s" % (userId,userUID,userName, userSurname)

date = datetime.date.today()
time = datetime.datetime.now().time()

print "CURRENT DATE: "
print date
print "CURRENT TIME: "
print time
print "\n"

#get classes that have todays date and time
sql3 = "SELECT * FROM CLASS WHERE tdate = '%s' AND '%s' >= stime AND etime >= '%s'" % (date.strftime('%Y-%m-%d'),time.strftime('%H:%M:%S'),time.strftime('%H:%M:%S'))

try:
	curs.execute(sql3)
	result2 = curs.fetchone()
except:
	print "Error: " + sql3

if result2 is None:
	print "There are no classes at this time today!"
else:
	classId = result2[0]
	className = result2[1]
	classDate = result2[2]
	classStart = result2[3]
	classEnd = result2[4]

	sql4 = "SELECT * FROM TIMETABLE WHERE classId = %s AND userId = %s" % (classId, userId)
	
	try:
		curs.execute(sql4)
		result3 = curs.fetchone()
	except:
		print "unable to access DB"
	
	if result3 is None: 
		print "You do not currently have class!"
	else:
		sql5 = "INSERT INTO ATTENDANCE VALUES(%d,%d)" % (classId,userId)
		try:
			curs.execute(sql5)

			print userName + " " + userSurname + " is noted as PRESENT in class: " + className + " date: "
			print classDate
			print " Starting at: "
			print classStart
			print " Ending at: "
			print classEnd 
		except:
			print "unable to insert presence in attendance table"



db.close()
