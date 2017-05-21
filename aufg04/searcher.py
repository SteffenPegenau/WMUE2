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
    if charset == "text/html":
        charset = "utf-8"
    print("Status: " + str(r.status) + "\t Charset: " + charset)
    if r.status != 200:
        print(r.data)
    return r.data.decode(charset)
    

class googleSearch:
    links = set()
    resultPagesToCrawl = set()
    crawledResultPages = set()


    def __init__(self):
        self.links = set()
        self.resultPagesToCrawl = set()
        self.crawledResultPages = set()

    def __extractResults(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        #f = open('google.html', 'w')
        #f.write(soup.prettify())
        #f.close()

        links = soup.select('h3.r a')
        #print(links)
        for link in links:
            href = link.get('href')
            #print(href)
            parsed = urlparse(href)
            params = parsed.query.split("&")
            for p in params:
                if p.startswith("q="):
                    url = p.split("=")[1]
                    self.links.add(url)
            #print(params)

    def __extractResultPagesToCrawl(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a.fl')
        print(links)
        for link in links:
            href = link.get("href")
            if href and href.startswith("/search"):
                print("Add href: " + href)
                url = "https://www.google.de" + href
                if not url in self.crawledResultPages:
                    self.resultPagesToCrawl.add(url)
        #print(self.resultPagesToCrawl)
            
    def writeResults(self):
        lines = ""
        for url in self.links:
            lines += url + "\n"
        f = open("google_result.txt", "w")
        f.write(lines)
        f.close()

    def searchFor(self, term):
        print("Search for " + term)
        term = term.replace(" ", "+")
        url = "https://www.google.de/search?q="  + term + "&ie=UTF-8&filter=0&oq=&gs_l=hp.1.0.35i39k1l6.0.0.0.1956.2.1.0.0.0.0.63.63.1.1.0....0...1..64.hp..1.1.62.6.natXrtk7oaU"

        html = getHTML(url)

        self.__extractResults(html)
        self.__extractResultPagesToCrawl(html)
        
        i = 1
        while len(self.resultPagesToCrawl) > 0:
            page = self.resultPagesToCrawl.pop()
            if not page in self.crawledResultPages:
                print("Crawl Page " + str(i))
                i = i + 1
                html = getHTML(page)
                self.__extractResults(html)
                print("Results now: " + str(len(self.links)))
                self.__extractResultPagesToCrawl(html)
                self.crawledResultPages.add(page)
                if page in self.resultPagesToCrawl:
                    self.resultPagesToCrawl.remove(page)
                self.writeResults()

        print("* Found " + str(len(self.links)) + " links")
        print("* " + str(len(self.crawledResultPages)) + " google pages crawled")
        print("* " + str(len(self.resultPagesToCrawl)) + " pages still to crawl")
        

google = googleSearch()
google.searchFor("darmstadt esoc jobs");

