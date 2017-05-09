#!/usr/bin/python3
import os
import hashlib
import cgi
import urllib3
http = urllib3.PoolManager()
htmlFolder = "html"

def hash(str):
    return hashlib.sha224(str.encode('utf-8')).hexdigest()

def save(url, data):
    # check whether save folder exists
    if not os.path.exists(htmlFolder):
        os.makedirs(htmlFolder)
    file = open(htmlFolder + "/" + hash(url) + ".html", "w")
    file.write(data)
    file.close()



def getUrlToFile(url):
    # Get data
    print("GET " + url, end="\tSTATUS ")
    r = http.request('GET', url)
    print(r.status)
    charset = r.headers['content-type'].split('charset=')[-1]
    save(url, r.data.decode(charset))

getUrlToFile("http://google.com")

