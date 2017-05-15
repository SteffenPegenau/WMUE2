#!/usr/bin/python3
import os
import hashlib
import cgi
import urllib3
import re
import mmap
from random import randint
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
urllib3.disable_warnings()
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

def alreadyCrawled(url):
    return os.path.exists(getPathForUrl(url))

def getUrlToFile(url):
    # Get data
    print("GET " + url, end="\tSTATUS ")

    try:
        r = http.request('GET', url)
        print(r.status)
        charset = r.headers['content-type'].split('charset=')[-1]
        try:
            save(url, r.data.decode(charset))
        except:
            print("ERROR: Invalid encoding: " + r.headers['content-type'])
    except:
        print("ERROR: can not fetch " + url)
    
    

def canonizeHref(url, href):
    parts = urllib3.util.parse_url(url)
    protocol = "http"
    if parts.scheme:
        protocol = parts.scheme
    
    host = ""
    if parts.host:
        host = parts.host
    else:
        print("NO HOST ERROR")
        exit()

    if href.startswith("//"):
        return "http:" + href
    elif href.startswith("/"):
        return protocol + "://" + host + href
    elif href.startswith("http"):
        return href
    else:
        return "ERROR: No rule for " + href
        

    #return protocol + "://" + host + "/"

def alreadyInList(url):
    if os.path.exists('links.txt') and url in open('links.txt').read():
        return True
    else:
        return False

def getLinks(url):
    path = getPathForUrl(url)
    if not os.path.exists(path):
        getUrlToFile(url)

    if os.path.exists(path):
        file = open(path, "r")
        soup = BeautifulSoup(file.read(), 'html.parser')
        file.close()
        links = soup.find_all('a')

        linkfile = open('links.txt', "a")
        for a in links:
            href = a.get('href')
            if href: #check for empty hrefs
                link = canonizeHref(str(url), href)
                if not link.startswith("ERROR") and not alreadyCrawled(link) and not alreadyInList(link):
                    linkfile.write(link + "\n")
        linkfile.close()
        #print(links)

def removeUrlFromLinks(url):
    f = open("links.txt","r+")
    d = f.readlines()
    d = list(set(d))
    f.seek(0)
    for i in d:
        if i != url and not alreadyCrawled(i): 
            f.write(i)
    f.truncate()
    f.close()

def getNextLink():
    f = open('links.txt')
    lines = f.readlines()
    num_lines = len(lines) - 1
    lineNo = randint(0, num_lines)
    f.close()
    return lines[lineNo]

#print(canonizeHref("http://", "/irgendwas"))

max = 3000
for i in range(0,max):
    url = getNextLink()
    print(str(i) + "/" + str(max), end="\t")
    getLinks(url.rstrip())
    removeUrlFromLinks(url)

#print(getNextLink())
#getLinks("http://www.tu-darmstadt.de/")

