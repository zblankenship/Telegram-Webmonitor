# Importing libraries 
import time 
import hashlib
import os
import pymongo
import cv2
import numpy as np
import datetime
import urllib
import math
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from urllib.request import urlopen, Request 
from dotenv import load_dotenv
from datetime import timedelta

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
    #for x in chatids:
    #    uri = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(token, x, message)
    #    requests.post(uri)

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

def get_screenshot(url, dbid):
    old_exists = '.\screenshots\\{}.png'.format(dbid)
    if os.path.exists(old_exists):
        path = '.\screenshots\\new_{}.png'.format(dbid)
        driver.get(url)
        time.sleep(2)
        driver.get_screenshot_as_file(path)
        driver.quit
    else:
        path = '.\screenshots\\{}.png'.format(dbid)
        driver.get(url)
        time.sleep(2)
        driver.get_screenshot_as_file(path)
        driver.quit

def check_if_same(current, new):
    current_image = cv2.imread(current)
    new_image = cv2.imread(new)

    if current_image.shape == new_image.shape:
        print("The images have same size and channels")
        difference = cv2.subtract(current_image, new_image)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) <= 10 and cv2.countNonZero(g) <= 10 and cv2.countNonZero(r) <= 10:
            print("The images are completely Equal")
            return True
        else:
            print("{} {} {}".format(cv2.countNonZero(b),cv2.countNonZero(g),cv2.countNonZero(r)))
            return False
    else:
        return False
            


#while True:
#    print("loop")
#    try:
headdoc = headcol.find()
start = time.process_time()
for x in headdoc:
    req = Request(url=x['url'])
    get_screenshot(x['url'], x['_id'])
    if os.path.exists('.\screenshots\\new_{}.png'.format(x['_id'])):
        print(x['url'])
        change = check_if_same('.\screenshots\\{}.png'.format(x['_id']), '.\screenshots\\new_{}.png'.format(x['_id']))
    else:
        continue
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