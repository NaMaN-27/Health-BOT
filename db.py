import pymysql 


host=''#enter host of db    
username=''#Enter username 
password=''# Enter password here 


db=pymysql.connect(host=host,user=username,password=password)
cursor=db.cursor()

cursor.execute("""CREATE DATABASE Health_Bot ;""")# change db name to the db name you want to  create
cursor.connection.commit()

cursor.execute("""USE Health_bot ;""")


cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                                    pid integer PRIMARY KEY auto_increment,
                                    email text NOT NULL,
                                    name text NOT NULL,
                                    password text NOT NULL,
                                    date DATE
                                    

                                    
                                );""")
cursor.connection.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS formdata(
                                    pid integer PRIMARY KEY auto_increment,
  
                                    dob text ,
                                    
                                    weight text ,
                                    height text ,
                                    gender text ,
                                    disease text ,
                                    medication text
                                    
                                    
                                );""")
cursor.connection.commit()

cursor.execute("show TABLES")
data=cursor.fetchall()
print(data)