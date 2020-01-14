import requests
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

locatii=[]
def scrapLocations(url):
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)


    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    list=soup.findAll("div", attrs={'class':'item-name'})

    for l in list:
        locatii.append(l.text.replace(" ","").replace("\t","").replace("\r","").replace("\n",""))

def writeFile(name,list):
    exportName='textData\\' + name + '.txt'
    if not os.path.isfile(exportName):
        with open(exportName, mode='a+',encoding="utf-8") as out:
            for item in list:
                out.write("%s\n" % item)


def scrapLocationsText(url,name):
    exportName = 'textData\\' + name + '.txt'
    if os.path.isfile(exportName):
        return

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)


    response = session.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    text=[]

    list=soup.find("div", attrs={'id':'mntl-chop_1-0--chop-content'})
    # print("TEXT FROM P")
    if list is None:
        return
    for p in list.findAll('p'):
        # print(p.text)
        text.append(p.text)

    writeFile(name,text)

    # print("TEXT FROM H1")
    for p in list.findAll('h1'):
        # print(p.text)
        text.append(p.text)


    # print("TEXT FROM H2")
    for p in list.findAll('h2'):
        # print(p.text)
        text.append(p.text)

    # print("TEXT FROM li")
    for p in list.findAll('li'):
        nots=['email',  'contact', 'website', 'Pin','share','like']
        ok=True
        for n in nots:
            if n.lower() in p.text.lower():
                ok=False
        if ok:
            # print(p.text)
            text.append(p.text)

    writeFile(name+"Extended",text)


    # for l in list:
    #     locatii.append(l.text.replace(" ","").replace("\t","").replace("\r","").replace("\n",""))



def main():
    print("Scrapping up to 33% of locations")
    scrapLocations('https://www.listchallenges.com/top-100-cities-of-europe')
    print("Scrapping up to 66% of locations")
    scrapLocations('https://www.listchallenges.com/top-100-cities-of-europe/list/2')
    print("Scrapping up to 99% of locations")
    scrapLocations('https://www.listchallenges.com/top-100-cities-of-europe/list/3')
    print("Finished scrapping of locations")

    print("Locations")
    for l in locatii:
        print(l+",")


    for l in locatii:
        sites=[]
        with open("data\\"+l.replace(',','')+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    print(row[-1])
                    sites.append(row[-1])
                    line_count += 1
            print(str(line_count)+" lines in :"+ l)



        for i in sites:
            scrapLocationsText(i,l)


main()
