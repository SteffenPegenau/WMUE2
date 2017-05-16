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
import pprint
import pickle
import string
#from sortedcontainers import SortedDict
urllib3.disable_warnings()
http = urllib3.PoolManager()
htmlFolder = "html"

def convertLinkCountToCsv(filename):
    haeufigkeiten = {}

    data = {}
    pkl_file = open(filename + '.pkl', 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()

    for hashKey,times in data.items():
        if times in haeufigkeiten:
            haeufigkeiten[times] = haeufigkeiten[times] + 1
        else:
            haeufigkeiten[times] = 1

    #pprint.pprint(haeufigkeiten)
    lines = "timesOfLinkReference;countOfTheseLinks\n"
    for times,howOften in sorted(haeufigkeiten.items()):
        lines += str(times) + ";" + str(howOften) + "\n"

    file = open(filename + ".csv", "w")
    file.write(lines)
    file.close()

def saveLinkCounter(url, filename):
    data = {}
    try:
        pkl_file = open(filename + '.pkl', 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
    except Exception as e:
        print("saveLinkCounter(): No file found")

    key = hash(url)

    if key in data:
        data[key] = int(data[key]) + 1
    else:
        data[key] = 1

    output = open(filename + '.pkl', 'wb')
    pickle.dump(data, output)
    output.close()

    convertLinkCountToCsv(filename)

def convertLinksPerPageCountToCsv():
    csv = open('linksPerPage.csv', 'w')

    lines = "countOfLinks;countOfPages\n"
    pkl_file = open('linksPerPage.pkl', 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()

    for links,pages in sorted(data.items()):
        lines += str(links) + ";" + str(pages) + "\n"

    csv.write(lines)
    csv.close()

def saveLinksPerPageCounter(count):
    data = {}
    try:
        pkl_file = open('linksPerPage.pkl', 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
    except Exception as e:
        print("saveLinksPerPageCounter(): No file found")

    #print("Vorher:")
    ##pprint.pprint(data)
    alias = count
    if alias in data:
        data[alias] = int(data[alias]) + 1
    else:
        data[alias] = 1

    #print("Nachher:")
    #pprint.pprint(data)

    output = open('linksPerPage.pkl', 'wb')
    pickle.dump(data, output)
    output.close()

    convertLinksPerPageCountToCsv()

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
            saveHostVisited(url)
        except:
            print("ERROR: Invalid encoding: " + r.headers['content-type'])
    except:
        print("ERROR: can not fetch " + url)

def getHostOfUrl(url):
    parts = urllib3.util.parse_url(url)
    if parts.host:
        # gibt z.B. www.etit.tu-darmstadt.de zurück
        #return parts.host
        hostparts = parts.host.split(".")
        tld = hostparts[-2] + "." + hostparts[-1]
        return tld

    else:
        print("NO HOST ERROR")
        exit()

def saveHostVisited(url):
    host = getHostOfUrl(url)

    data = {}
    try:
        pkl_file = open('hosts.pkl', 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
    except Exception as e:
        print("saveHostVisited(): No file found")

    #print("Vorher:")
    ##pprint.pprint(data)
    alias = host
    if alias in data:
        data[alias] = int(data[alias]) + 1
    else:
        data[alias] = 1

    #print("Nachher:")
    #pprint.pprint(data)

    output = open('hosts.pkl', 'wb')
    pickle.dump(data, output)
    output.close()

    lines = "host;visits\n"
    for host,count in data.items():
        lines += host + ";" + str(count) + "\n"
    f = open("hosts.csv", "w")
    f.write(lines)
    f.close()

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
        htmlraw = file.read()
        soup = BeautifulSoup(htmlraw, 'html.parser')
        file.close()
        links = soup.find_all('a')
        saveLinksPerPageCounter(int(len(links)))

        linkfile = open('links.txt', "a")
        for a in links:
            href = a.get('href')
            if href: #check for empty hrefs
                link = canonizeHref(str(url), href)
                saveLinkCounter(link, "unfilteredLinks")
                if not link.startswith("ERROR") and not alreadyCrawled(link) and not alreadyInList(link):
                    linkfile.write(link + "\n")
        linkfile.close()

        l = soup.select("[class*='nav']")
        [s.extract() for s in l]
        links = soup.find_all('a')
        for a in links:
            href = a.get('href')
            if href: #check for empty hrefs
                link = canonizeHref(str(url), href)
                saveLinkCounter(link, "filteredLinks")

        #saveLinksPerPageCounter(int(len(links)))
        #print(part)

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

max = 5000
for i in range(0,max):
    url = getNextLink()
    print(str(i) + "/" + str(max), end="\t")
    getLinks(url.rstrip())
    removeUrlFromLinks(url)

#print(getNextLink())
#getLinks("http://www.tu-darmstadt.de/")
