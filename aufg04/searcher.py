#!/usr/bin/python3
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
http = urllib3.PoolManager()
from urllib.parse import urlparse

searchterm="esa darmstadt"

def getHTML(url):
    print("Calling " + url, end='\t')
    r = http.request('GET', url)
    charset = r.headers['content-type'].split('charset=')[-1]
    print("Status: " + str(r.status) + "\t Charset: " + charset)
    return r.data.decode(charset)
    

class googleSearch:
    links = set()
    resultPages = set()


    def __init__(self):
        self.links = set()
        self.resultPages = set()

    def __extractResults(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        f = open('google.html', 'w')
        f.write(soup.prettify())
        f.close()

        links = soup.select('h3.r a')
        #print(links)
        for link in links:
            href = link.get('href')
            parsed = urlparse(href)
            params = parsed.query.split("&")
            for p in params:
                if p.startswith("q="):
                    url = p.split("=")[1]
                    self.links.add(url)
            #print(params)

    def __extractResultPages(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a.fl')
        print(links)
            


    def searchFor(self, term):
        print("Search for " + term)
        term = term.replace(" ", "+")
        url = "https://www.google.de/search?q="  + term + "&ie=UTF-8"

        html = getHTML(url)

        #self.__extractResults(html)
        self.__extractResultPages(html)
        print(self.links)

google = googleSearch()
google.searchFor("esa darmstadt");

