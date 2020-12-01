#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 16:26:33 2020

@author: elvyyang
"""


from bs4 import BeautifulSoup
from selenium import webdriver
import json
import os, os.path
import ast

# chrome_path = r'/Users/elvyyang/Downloads/chromedriver' #path from 'which chromedriver'
# driver = webdriver.Chrome(executable_path=chrome_path)
chrome_path = "/Users/elvyyang/Downloads/chromedriver"
startingUrl = '/catalog/HistoryattheBodleian/hfl'
BASE_URL = "http://www.librarything.com"

title_to_details_href = {}
book_data = {}

#returns the parsed html
def getSoup(driver):
    html = driver.page_source
    return BeautifulSoup(html)

# get url and wait for it to load
def getUrl(driver, url, seconds = 15):
    driver.get(url)
    driver.implicitly_wait(seconds)


class PageCrawler(object):
    def __init__(self, startingURL, baseURL):
        self.startingURL = startingURL
        self.BASE_URL = baseURL
        self.driver = webdriver.Chrome(executable_path=chrome_path)
        

    def openPage(self):
        '''
        Opens the first page of the website and obtains the href for each 
        subsequent page link up to page 109.
        pageList contains the href links

        Returns
        -------
        None

        '''
        global pageList
        pageList = []
        
        getUrl(self.driver, self.BASE_URL + self.startingURL)
        soup = getSoup(self.driver)
        frames = soup.find_all("frame", attrs={'name': 'bottom'}) 
        frameUrl = frames[0]["src"]
        newUrl = BASE_URL + frameUrl
        getUrl(self.driver, newUrl)
        nextPageSoup = getSoup(self.driver)
        getList = nextPageSoup.find_all("td",{"id": "pages2"})
        page = getList[0].find_all("a")
        pageList.append(frameUrl)
        for i in range(len(page)):
            pageList.append(page[i].get("href"))
            
    def iteratePages(self): 
        '''
        From pageList iterates extractTitleList

        Returns 
        -------
        extractTitleList

        '''
        for i in range(len(pageList)):
            getUrl(self.driver, self.BASE_URL + pageList[i])
            pageCrawler.extractTitleList(i)
            
    def extractTitleList(self, pageNumber):
        '''
        From pageList, opens each title's details page and obtains title and details href. 
        saves information in json files

        title_to_details_href : dictionary {title: details_href}
        titleList : list [titles]
            
        Parameters
        ----------
        pageNumber : page numbers are indexed by 0 and used to name the json files
        
        Returns 
        -------
        files containing {title: title-href} dictionary in title_to_urls folder

        '''
        
        bookSoup = getSoup(self.driver)
        books = bookSoup.find_all("a", class_="lt-title")
        book_details = bookSoup.find_all("a", href = lambda x : x and "details" in x)
        
   
        global title_to_details_href
        title_to_details_href = {}
        global titleList
        titleList=[]

        for i in range(len(books)):
            title = books[i].decode_contents()
            titleList.append(title)
            details_href = book_details[i].get("href");
            title_to_details_href[title] = BASE_URL +  details_href
        
        #takes file name and dumps library into file 
        fileName = "title_to_urls/" + str(pageNumber) + ".json"
        with open(fileName, "w") as write_file:
            json.dump(title_to_details_href, write_file)
    
            
    def iterateBooks(self):
        '''
        Iterates through json files in title_to_urls
        runs extractDetails for each title 
        appends Details to library 
        saves library to json files in book_data folder
        
        library: dictionary {title: Details}

        Returns 
        -------
        files containing library 

        '''
        dirName = "./title_to_urls/"
        #for each Json file in title_to_urls folder
        files = []
        Files = os.listdir(dirName)
        for filename in Files:
            if filename.endswith(".json"):
                files.append(os.path.join(dirName, filename))
        
        for file in files:
            library = {}
            with open(file,'r') as reader:
                contents = reader.read()
                fileDict = ast.literal_eval(contents)
                for title in fileDict:
                    details = pageCrawler.extractDetails(fileDict[title])
                    library[title] = details
            fileName = "book_data/" + file.strip("./title_to_urls/")                         
            with open(fileName, "w") as write_file:
                json.dump(library, write_file)
 
    def extractDetails(self, title_url):
        '''
        Goes to url for each title and scrapes author, publication, and isbn information
        
        
        Parameters
        ----------
        title_url : full href to each title

        Returns
        -------
        Details : list [author, publication, isbn]

        '''
        Details = []
       
        getUrl(self.driver, title_url)
        detailSoup = getSoup(self.driver)
        isbns = detailSoup.find_all("td", {"id": "bookedit_ISBN"})
        isbn = isbns[-1].decode_contents()
        isbn = sliceISBN(isbn)
        authors = detailSoup.find_all("a", href = lambda x : x and "author" in x)
        author = authors[0].decode_contents()
        publications = detailSoup.find_all("td", {"id": "bookedit_publication"})
        publication = publications[-1].decode_contents()
        Details.append((author,publication,isbn))
        return Details
          
def sliceISBN(isbn):
    ind = isbn.index("/")
    return isbn[ind:]
            
                
pageCrawler = PageCrawler(startingUrl, BASE_URL)
pageCrawler.openPage()
pageCrawler.iteratePages()
pageCrawler.iterateBooks()



