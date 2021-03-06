# Importing libraries 
import time 
import hashlib
from urllib.request import urlopen, Request 

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

url = GetWebsite('https://twitter.com/Okz899')
response = GetRespone(url)
currentHash = GenerateHash(response)
print("Running")
SleepTime(10)

while True:
    try:
        print('loop')
        response = urlopen(url).read()
        newHash = GenerateHash(response)
        SleepTime(10)
        if newHash == currentHash: 
            continue
        else: 
            ChangeNotification(url)
            currentHash = newHash
    except Exception as e: 
    	print("error") 