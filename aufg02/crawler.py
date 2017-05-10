#!/usr/bin/python3
import os
import hashlib
import cgi
import urllib3
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
http = urllib3.PoolManager()
htmlFolder = "html"

def hash(str):
    return hashlib.sha224(str.encode('utf-8')).hexdigest()

def getPathForUrl(url):
    return htmlFolder + "/" + hash(url) + ".html"

def save(url, data):
    # check whether save folder exists
    if not os.path.exists(htmlFolder):
        os.makedirs(htmlFolder)
    file = open(getPathForUrl(url), "w")
    file.write(data)
    file.close()

def getUrlToFile(url):
    # Get data
    print("GET " + url, end="\tSTATUS ")
    r = http.request('GET', url)
    print(r.status)
    charset = r.headers['content-type'].split('charset=')[-1]
    save(url, r.data.decode(charset))

def getLinks(url):
    path = getPathForUrl(url)
    if not os.path.exists(path):
        getUrlToFile(url)

    file = open(path, "r")
    soup = BeautifulSoup(file.read(), 'html.parser')
    file.close()
    links = soup.find_all('a')
    for a in links:
        print(a.get('href'))
    #print(links)

getLinks("http://heise.de")
#getUrlToFile("http://google.com")

