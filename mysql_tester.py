import mysql.connector

SQL_HOST_IP = "192.168.20.217"
SQL_USER="don"
SQL_PASSWORD="girman888"
SQL_DATABASE='radio'

mydb = mysql.connector.connect(
  host=SQL_HOST_IP, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE
)

mycursor = mydb.cursor(buffered=True)

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

''''''
#Make project database
mycursor.execute("DROP TABLE IF EXISTS log")
mycursor.execute("DROP TABLE IF EXISTS settings")

mycursor.execute("CREATE TABLE log (mykey INTEGER(100) NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                 "mydatetimestamp VARCHAR(255) DEFAULT CURRENT_TIMESTAMP, "
                 "mydata VARCHAR(300))")

mycursor.execute("CREATE TABLE settings (mykey INTEGER(100) NOT NULL AUTO_INCREMENT PRIMARY KEY, mydatetimestamp VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,platform VARCHAR(255), "
                 "frequency_a VARCHAR(255), frequency_b VARCHAR(255), serial_number VARCHAR(255), mode VARCHAR(255), MicGain VARCHAR(255), "
                 "Rec1SquelchLevel VARCHAR(255), Rec2SquelchLevel VARCHAR(255), "
                 "NoiseBlanker1 VARCHAR(255), NoiseBlanker2 VARCHAR(255), NoiseBlankerLevel1 VARCHAR(255), NoiseBlankerLevel2 VARCHAR(255), OmOptionsInstalled VARCHAR(255), "
                 "RecieverPreamp1 VARCHAR(255), RecieverPreamp2 VARCHAR(255), ReqPowerOut_Watts VARCHAR(255), PowerOut_Watts VARCHAR(100),"
                 "RecieverAttenuator1 VARCHAR(100), RecieverAttenuator VARCHAR(100), TranscPowerStatus VARCHAR(255), RFGain1 VARCHAR(255), RFGain2 VARCHAR(255), "
                 "HResolutionSmeter VARCHAR(255), SquelchLevel1 VARCHAR(255),SquelchLevel2 VARCHAR(255), SWR VARCHAR(255), "
                 "RecievedTextCount VARCHAR(255), TransmittedTextCount VARCHAR(255), TransmitMeterMode VARCHAR(100), TransmitQuery VARCHAR(100), "
                 "VOXState VARCHAR(100), XFILNumber1 VARCHAR(100), XFILNumber2 VARCHAR(100), XITControl VARCHAR(100), AgcTimeConstant VARCHAR(100))")
mydb.commit()
'''#mycursor.execute("CREATE TABLE log (name VARCHAR(255), dataline VARCHAR(255))")

sql = "INSERT INTO log (name, dataline) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

sql = "INSERT INTO log (name, dataline) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]

mycursor.executemany(sql, val)

mydb.commit()

mycursor.execute("SELECT * FROM log")

myresult = mycursor.fetchall()
mydb.commit()

for x in myresult:
  print(x)

mycursor.execute("SELECT * FROM log")

myresult = mycursor.fetchone()
mydb.commit()
print()
print(myresult)


mycursor.execute("DELETE * FROM log ")
mydb.commit()
'''

mysql = "INSERT INTO log (mydata) VALUES ('test')"
mycursor.execute(mysql)

mysql = "INSERT INTO log (mydata) VALUES (%s)"
data = ['testxxx']

mycursor.execute(mysql,data)

testdata = 'test555555555'
mysql = "INSERT INTO log SET mydata='" + testdata + "'"
print(mysql)
mycursor.execute(mysql)
mydb.commit()

mycursor.execute("SELECT * FROM log")
myresult = mycursor.fetchone()
print()
print(myresult)

mycursor.execute("SELECT * FROM log")
myresult = mycursor.fetchall()
mydb.commit()

for x in myresult:
  print(x)


#mycursor.execute("DELETE FROM log")

mydb.commit()

