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
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


load_dotenv('key.env')
mongo = os.getenv('mongo')
token = os.getenv('token')
myclient = pymongo.MongoClient(mongo)
mydb = myclient["webmonitor"]
headcol = mydb["websites"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
chatids = []
options = Options()
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(options=options, executable_path="C:\Selenium\geckodriver.exe")
i = 0

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
        requests.post(uri)

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

def get_screenshot(url, i):
    driver.get(url)
    time.sleep(1)
    path = 'C:\\Users\\zackb\\Documents\\Projects\\Telegram-Webmonitor\\screenshots\\{}.png'.format(i)
    print(path)
    driver.get_screenshot_as_file(path)
    driver.quit


#while True:
#    print("loop")
#    try:
headdoc = headcol.find()
start = time.process_time()
for x in headdoc:
    req = Request(url=x['url'])
    get_screenshot(x['url'], i)
    i = i + 1
    try:
        response = urlopen(req).read()
    except urllib.error.HTTPError as e:
        if e.code in (..., 403, ...):
            continue
    newHash = GenerateHash(response)
    if newHash == x['hash']: 
        updatetime(x['url'])
    else: 
        ChangeNotification(x['url'], token)
        updatehash(x['url'],newHash)
time_taken = SleepTime(start)
#    except Exception as e: 
#        print("error")
#        continue