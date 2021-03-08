# Importing libraries 
import time 
import hashlib
import os
import pymongo
from urllib.request import urlopen, Request 
from dotenv import load_dotenv
from datetime import timedelta, datetime
import datetime
import urllib
import math
import requests

load_dotenv('key.env')
mongo = os.getenv('mongo')
token = os.getenv('token')
myclient = pymongo.MongoClient(mongo)
mydb = myclient["webmonitor"]
headcol = mydb["websites"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
chatids = []

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

def SleepTime(start_time):
    time_taken = time.process_time() - start
    time_taken = math.ceil(time_taken)
    time_to_sleep = 300 - time_taken
    time.sleep(time_to_sleep)
    return time_taken

def ChangeNotification(url, token):
    chatids = get_chat_ids(url)
    message = 'The website you are monitoring has changed:{}'.format(url)
    for x in chatids:
        uri = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, x, message)
        print(uri)
        requests.post(uri)
    print(url, 'changed')

def updatetime(url):
    time = timefunc()
    date = datefunc()
    date_time = date + " " + time
    myquery = { "url": url }
    newvalues = { "$set": { "time_last_checked": date_time } }
    headcol.update_one(myquery, newvalues)

def updatehash(url,hash):
    time = timefunc()
    date = datefunc()
    date_time = date + " " + time
    myquery = { "url": url }
    newvalues = { "$set": { 
            "hash": hash,
            "last_change_time": date_time,
            "time_last_checked": date_time} }
    headcol.update_one(myquery, newvalues)

def timefunc():
    time = datetime.datetime.now()
    time = time.strftime("%X")
    return time

def datefunc():
    date = datetime.datetime.now()
    date = date.strftime("%x")
    return date

def get_chat_ids(url):
    chatids = []
    currentcol = mydb[url]
    currentdoc = currentcol.find()
    for x in currentdoc:
        chatids.append(x['chats_id_to_notify'])
    return chatids


while True:
    print("loop")
    try:
        headdoc = headcol.find()
        start = time.process_time()
        for x in headdoc:
            print('......................................')
            print(x['url'])
            req = Request(url=x['url'])
            try:
                response = urlopen(req).read()
            except urllib.error.HTTPError as e:
                if e.code in (..., 403, ...):
                    continue
            newHash = GenerateHash(response)
            print("New Hash: " + newHash)
            print("Old Hash: " + x['hash'])
            if newHash == x['hash']: 
                updatetime(x['url'])
            else: 
                ChangeNotification(x['url'], token)
                updatehash(x['url'],newHash)
            print('......................................')
        time_taken = SleepTime(start)
    except Exception as e: 
        print("error")
        continue