import pymongo

myclient = pymongo.MongoClient("mongodb+srv://zblankenship:DZMvvR54VOqdEwUw@cluster0.jpyfe.mongodb.net/defaults?retryWrites=true&w=majority")

mydb = myclient["webmonitor"]
mycol = mydb["websites"]