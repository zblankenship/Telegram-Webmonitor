# Importing libraries 
import time 
import hashlib
import os
import pymongo
from urllib.request import urlopen, Request 
from dotenv import load_dotenv
from datetime import timedelta, datetime

load_dotenv('key.env')
mongo = os.getenv('mongo')
myclient = pymongo.MongoClient(mongo)
mydb = myclient["webmonitor"]
headcol = mydb["websites"]

def GetWebsite(link):
    url = Request(link, 
			headers={'User-Agent': 'Mozilla/5.0'}) 
    return url

def GetRespone(url):
    response = urlopen(url).read()
    return response

def GenerateHash(data):
    currentHash = hashlib.sha224(response).hexdigest() 
    return currentHash

def SleepTime(length):
    time.sleep(length)

def ChangeNotification(link):
    print(link, 'changed')

def updatetime(url):
    time = timefunc()
    date = datefunc()
    date_time = date + time
    myquery = { "url": url }
    newvalues = { "$set": { "time_last_checked": date_time } }
    mycol.update_one(myquery, newvalues)

def updatehash(url,hash):
    time = timefunc()
    date = datefunc()
    date_time = date + time
    myquery = { "url": url }
    newvalues = { "$set": { 
            "hash": hash,
            "last_change_time": date_time } }
    mycol.update_one(myquery, newvalues)


def timefunc():
    time = datetime.datetime.now()
    time = time.strftime("%X")
    return time

def datefunc():
    date = datetime.datetime.now()
    date = date.strftime("%x")
    return date


while True:
    try:
        headdoc = headcol.find()
        for x in headdoc:
            print('loop')
            response = urlopen(x['url']).read()
            newHash = GenerateHash(response)
            if newHash == x['hash']: 
                updatetime(x['url'])
            else: 
                ChangeNotification(url)
                updatehash(x['url'],x['hash'])
    except Exception as e: 
    	print("error") 



