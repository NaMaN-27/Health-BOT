
import datetime
import smtplib
import sqlite3
from random import randint

import boto3
import pymysql
from flask import Flask, redirect, render_template, request, url_for
from keras.preprocessing import image
from keras.preprocessing.image import load_img

import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
import nltk
from difflib import get_close_matches
import keras
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import Xception
import csv
nltk.download('wordnet')
import requests
import json
import pandas as pd





ps = PorterStemmer()
with open('models\sym_dis_map_base.json', 'r') as fire:
  
  dict1 = json.load(fire)

jrr = pd.read_csv('models\Symptom_severity.csv')#change




model = load_model("models\disease_model.h5")

precautionDictionary = {}
description_list = {}
def getprecautionDict():
    global precautionDictionary
    with open('models\symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)


def getDescription():
    global description_list
    with open('models\symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)

getprecautionDict()
getDescription()


def finder(i):
  j = wordnet.synsets(i.lower())
  for k in j:
    k = k.lemma_names()
    for m in k:
      if m.lower() in dict1.keys():
        return dict1[m.lower()]
      elif ps.stem(m) in dict1.keys():
        return dict1[ps.stem(m)]
  j = wordnet.synsets(ps.stem(i))
  for k in j:
    k = k.lemma_names()
    for m in k:
      if m.lower() in dict1.keys():
        return dict1[m.lower()]
  if i.lower() in dict1.keys():
    return dict1[i.lower()]
  elif ps.stem(i) in dict1.keys():
    return dict1[ps.stem(i)]
  z = get_close_matches(i.lower(), list(dict1.keys()),  n=3, cutoff= 0.4)
  if len(z) > 0:
    i = dict1[z[0]]
  return i


def image_predict(path):
  image_model=load_model("models\FINALMODELDISEASECLASSIFICATION.h5")
  image = load_img(path, target_size=(227, 227))
  img = np.array(image)
  img = img / 255.0
  img = img.reshape(1,227,227,3)
  class_names = ['Covid', 'NORMAL', 'PNEUMONIA', 'TB']
  label = image_model.predict(img)
  predicted_label = np.argmax(label)
  

  return str(class_names[predicted_label])


def get_response(inpu,user):
  response = client.post_text(botName="HealthCare",botAlias='naman',userId=user,inputText=inpu)
  
  return response['message']


def mail(date_time,u_mail):
  patient_email=u_mail
  server=smtplib.SMTP_SSL("smtp.gmail.com",465)
  doc_email=" " #change
  server.login("","")#change
  randomhash=str(randint(100,999999))
  link="https://helthkare.000webhostapp.com/#"+randomhash
  messdoc=messpt="Subject : HealthCare video consultancy \n\n We have scheduled an appointment with you. Please join the provided link at "+date_time[1]+" on "+date_time[0]+".\n"+link
  messpt="Subject : HealthCare video consultancy \n\n We are glad you scheduled an online appointment with us. Please join the provided link at "+date_time[1]+" on "+date_time[0]+".\n"+link
  server.sendmail("",patient_email,messpt)#change
  server.sendmail("",doc_email,messpt)#change
  print(u_mail)


def val_otp(user_mail):
  
  server=smtplib.SMTP_SSL("smtp.gmail.com",465)
  
  server.login("","")#change
  randomhash=str(randint(1000,9999))
  
  
  messpt="Subject : HealthCare video consultancy \n\n We are glad you have signed up on our website . Here is the OTP "+randomhash
  server.sendmail("helthkare@gmail.com",user_mail,messpt)
  print(randomhash)
  return randomhash



"""MAP API"""

URL = "https://discover.search.hereapi.com/v1/discover"
# latitude = g.latlng[0]
# longitude = g.latlng[1]
latitude =18.5074
longitude=73.807
api_key = 'oq0GkZ7rld2zgcxuOM5-Tq3eGQRQQvDj-nnlDz0V7BE' # Acquire from developer.here.com
query = 'hospital'
limit = 5

PARAMS = {
            'apikey':api_key,
            'q':query,
            'limit': limit,
            'at':'{},{}'.format(latitude,longitude)
         } 

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
data = r.json()


hospitalOne = data['items'][0]['title']
hospitalOne_address =  data['items'][0]['address']['label']
hospitalOne_latitude = data['items'][0]['position']['lat']
hospitalOne_longitude = data['items'][0]['position']['lng']


hospitalTwo = data['items'][1]['title']
hospitalTwo_address =  data['items'][1]['address']['label']
hospitalTwo_latitude = data['items'][1]['position']['lat']
hospitalTwo_longitude = data['items'][1]['position']['lng']

hospitalThree = data['items'][2]['title']
hospitalThree_address =  data['items'][2]['address']['label']
hospitalThree_latitude = data['items'][2]['position']['lat']
hospitalThree_longitude = data['items'][2]['position']['lng']


hospitalFour = data['items'][3]['title']
hospitalFour_address =  data['items'][3]['address']['label']
hospitalFour_latitude = data['items'][3]['position']['lat']
hospitalFour_longitude = data['items'][3]['position']['lng']

hospitalFive = data['items'][4]['title']
hospitalFive_address =  data['items'][4]['address']['label']
hospitalFive_latitude = data['items'][4]['position']['lat']
hospitalFive_longitude = data['items'][4]['position']['lng']


"""MAP API"""



app = Flask(__name__)

ACCESS_ID="" #change
ACCESS_KEY=""#change
client = boto3.client('lex-runtime',region_name='us-east-1',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
host=''#change "This is the host of the db "
username=''#db username 
password=''#db pass
db=pymysql.connect(host=host,user=username,password=password)
cursor=db.cursor()
cursor.execute("""USE HealthBOT ;""") # change db name to the db name you have created

sym=False
symptons=[]
err_list = []
user_name=" "  
user_otp=""
user_email=""
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login",methods = ['POST','GET'])
def login():
  global cursor
  global user_name
  global user_email
  if request.method=='POST':
    login_data=request.get_json('login_data')
    print(login_data)
    cursor.execute(""" select name, email from users where email="{}" and password="{}"; """ .format(login_data[0],login_data[1]) )
    result=cursor.fetchall()
    print(result)
    if len(result)==1:
      user_name=result[0][0]
      user_email=login_data[0]
      return "success"
    else:
      return "INCORRECR USERNAME AND PASSOWORD"
  if request.method=='GET':
    return render_template("index.html")


@app.route("/logout")
def logout():
    return render_template("login.html")


@app.route("/date",methods = ['POST','GET'])
def date():
  global user_email
  if request.method=='POST':
    date_time=request.get_json('dateandtime')
    mail(date_time,user_email)
    return "We Have Scheduled Your appointment with doctor . Thanks for contacting Us ."


@app.route("/signup",methods = ['POST','GET'])
def signup():
  global cursor
  global user_name
  global user_otp
  if request.method=='POST':
    signup_data=request.get_json('signup_data')
    print(signup_data)
    
    
    cursor.execute(""" select email from users where email="{}" ;""".format(signup_data[2])  )
    result=cursor.fetchall()
    
    if len(result)==0 and str(signup_data[3])==user_otp and user_otp!="":
      

      

      currentDateTime = datetime.datetime.now()
      
      cursor.execute(''' INSERT INTO users(email,name,password,date)  
                  VALUES("{}","{}","{}","{}") ;'''.format(signup_data[2],signup_data[0],signup_data[1],currentDateTime ))
      cursor.connection.commit()
      
      user_name=signup_data[0]
      return "success"

    else :
      return "WRONG OTP"

  if request.method=='GET':
    return render_template("index.html")


@app.route("/getotp",methods = ['POST','GET'])
def getotp():
  global user_otp
  if request.method=='POST':
    signup_data=request.get_json('signup_data')
    cursor.execute(""" select email from users where email="{}" ;""".format(signup_data[2])  )
    result=cursor.fetchall()
    
    if len(result)==0:
      
      user_otp=val_otp(signup_data[2])
      return "success"
    else :
      return "EMAIL EXISTS"




@app.route("/new_form",methods = ['POST','GET'])
def new_form():
  if request.method=='POST':
    data=request.get_json('form_data')
    print(data)
    dis=""
    med=""
    for i in data[4].keys():
      dis=dis+"_"+i+"_"+data[4][i]+"_"
    
    for i in data[5]:
      med=med+"_"+i+"_"
    
    dis=dis[1:len(dis)-1]
    med=med[1:len(med)-1]
    print(dis)
    print(med)

    cursor.execute(''' INSERT INTO formdata(dob,weight,height,gender,disease,medication)  
                  VALUES("{}","{}","{}","{}","{}","{}") ;'''.format(data[0],data[1],data[2],data[3],dis,med ))
    cursor.connection.commit()


    return "ok"
  if request.method=='GET':
    return render_template("registrationform.html")




@app.route('/pred', methods=["GET", "POST"])
def model_pred():
  return render_template("model.html")


@app.route('/submit', methods=["GET", "POST"])
def output():
  if (request.method == "POST"):
    
    path="Saved_images\\"
    
    img = request.files["image"]
    
    
    img_path = path + img.filename
    img.save(img_path)
    
    res=image_predict(img_path)
    
    return "The prediction is " + res 


@app.route("/chat",methods = ['POST'])
def chat():
  global user_name                                                                          
  global sym
  global symptons
  global precautionDictionary
  global description_list
  input=request.get_json('input_chat')[0]
  response=get_response(input,user_name)
  if response=="Sure, on what date would you like me to schedule your online appointment.":
    return response

  if response=="What are your symptoms?":
    sym=True

  if sym:
    
    if input.lower()!="yes" and input.lower()!="no":
      symptons.append(input)
    if input=="no":
      err_empty = True
      symptons.pop(0)
      k2 = pd.read_csv("models\symp.csv", index_col=0)
      k2 = k2.replace(1,0)
      y2 = pd.read_csv("models\dis.csv", index_col=0)
      symptons_set=set(symptons)
      sym=False
      for inpu in symptons_set:
        inpu2 = inpu.lower().split(' ')
        inpu = finder(inpu2[0])
        
        for i in range(1,len(inpu2)):
          inpu += "_" + finder(inpu2[i])
        if(inpu in symp_list_1):
          k2[inpu] = 1
          
          continue
        z = get_close_matches(inpu, symp_list_1,  n=3, cutoff= 0.8)
        if len(z) > 0:
          
          k2[z[0]] = 1
        else:
          err_list.append(inpu)
          err_empty = False
          
      ans = model.predict(k2)
      j = y2.columns
      response = "The Chatbot  predicts your diagnosis to be : " + str(j[np.argmax(ans)]) + " \n \n"
      print(description_list)
      response += description_list[str(j[np.argmax(ans)])] + "\n"
      precution_list=precautionDictionary[str(j[np.argmax(ans)])]
      response += "Take following measures : \n"
      for  i,j in enumerate(precution_list):
        response += str(i+1) + ")" + str(j) + "\n"
      k2 = k2.replace(1,0)
      if not err_empty:
        pass
        
      symptons.clear()
      err_list.clear()

  return response


@app.route('/map')
def map_func():
	return render_template('map.html',
                            latitude = latitude,
                            longitude = longitude,
                            apikey=api_key,
                            oneName=hospitalOne,
                            OneAddress=hospitalOne_address,
                            oneLatitude=hospitalOne_latitude,
                            oneLongitude=hospitalOne_longitude,
                            twoName=hospitalTwo,
                            twoAddress=hospitalTwo_address,
                            twoLatitude=hospitalTwo_latitude,
                            twoLongitude=hospitalTwo_longitude,
                            threeName=hospitalThree,
                            threeAddress=hospitalThree_address,
                            threeLatitude=hospitalThree_latitude,
                            threeLongitude=hospitalThree_longitude,
                            fourName=hospitalFour,		
                            fourAddress=hospitalFour_address,
                            fourLatitude=hospitalFour_latitude,
                            fourLongitude=hospitalFour_longitude,
                            fiveName=hospitalFive,		
                            fiveAddress=hospitalFive_address,
                            fiveLatitude=hospitalFive_latitude,
                            fiveLongitude=hospitalFive_longitude
                            )



if __name__ == '__main__':
   app.run()
