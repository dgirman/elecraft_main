import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.20.217",
  user="don",  password="girman888", database='radio'

)

mycursor = mydb.cursor(buffered=True)

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x)

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
sql = "INSERT INTO log (data) VALUES %s"
val = [
   'Lowstreet 4',
  'Apple st 652',
   'Mountain 21'
]
mycursor.execute("SELECT * FROM log")

myresult = mycursor.fetchone()
print()
print(myresult)

mycursor.execute("SELECT * FROM log")

myresult = mycursor.fetchall()
mydb.commit()

for x in myresult:
  print(x)
