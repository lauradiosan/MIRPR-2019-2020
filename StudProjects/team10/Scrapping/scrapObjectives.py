import requests
import urllib
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
import csv
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os


locatii=[]

import time





def writeFile(name,dict):
    exportName='linksData\\' + name + '.txt'
    with open(exportName, mode='a+',encoding="utf-8") as out:
        for item in dict:
            print(item['name'] +';'+item['review'] +';'+item['top'] +';'+item['link']+';\n')
            out.write(item['name'] +';'+item['review'] +';'+item['top'] +';'+item['link']+';\n')

def writeLocation(name,dict):
    exportName='obiectiveData\\' + name + '.txt'
    with open(exportName, mode='a+',encoding="utf-8") as out:
        for item in dict:
            try:
                out.write(item['name'] +';'+item['review'] +';'+item['top'] +';'+item['link']+
                          ';'+str(item['category'])+';'+item['description']+';'+str(item['schedule'])+
                          ';'+item['duration']+';'+item['coordinates'][0]+';'+item['coordinates'][1]+';\n')
            except:
                print("FAILED\n\n\n\n")

def scrapVisitText(url,name):
    # exportName = 'textData\\' + name + '.txt'
    # if os.path.isfile(exportName):
    #     return

    #CHOICE 1
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    #
    #
    # response = session.get(url)


    # CHOICE 2
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source




    soup = BeautifulSoup(html, "html.parser")

    textCategory=[]
    # print(response.text)

    # ----------------------------------------------------
    try:
        list=soup.find("div", attrs={'class':'detail'})
        # print("TEXT FROM P")
        if list is None:
            pass
        else:
            for p in list.findAll('a'):
                # print(p.text)
                textCategory.append(p.text)
            try:
                textCategory.remove("More")
            except:
                pass

        # print(textCategory)
    except:
        pass


    # ----------------------------------------------------
    descriptionCategory = ""

    try:
        list = soup.findAll("div", attrs={'class': 'attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--1_Efg'})
        # print("TEXT FROM P")
        if list is None:
            pass
        else:
            # print(p.text)
            descriptionCategory=list[1].text

            # print(descriptionCategory)
    except:
        pass


    # ----------------------------------------------------
    durationCategory = ""
    try:
        list = soup.findAll("div", attrs={'class': 'attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--1_Efg'})
        # print("TEXT FROM P")
        if list is None:
            pass
        else:
            # print(p.text)
            durationCategory=list[4].text.split(':')[-1]

            # print(durationCategory)
    except:
        pass


    # ----------------------------------------------------
    scheduleCategory = []

    try:
        list = soup.find("div", attrs={'class': 'hoursAll hidden'})

        try:
            list=soup.find("div",attrs={'class': 'ui_columns is-multiline'})
            # print("FOUND")
        except:
            pass
        # print("TEXT FROM P")
        if list is None:
            pass
        else:
            # print(p.text)
            scheduleCategory=[x.text for x in list]

            # print(scheduleCategory)
    except:
        pass

    # ----------------------------------------------------
    coordinatesCategory = ["",""]

    try:
        list = soup.find("div", attrs={'class': 'prw_rup prw_common_responsive_static_map_image staticMap'})


        # print("TEXT FROM P")
        if list is None:
            pass
        else:
            # print(p.text)
            coordinatesCategory=list.contents[1]['src'].split("center=")[1].split('&')[0].split(',')

            # print(coordinatesCategory)
    except:
        pass


    print("__________________")
    driver.close()
    return textCategory,durationCategory,scheduleCategory,coordinatesCategory,descriptionCategory





def scrapLinks(url,obiective):
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.get(url)
    html = driver.page_source




    soup = BeautifulSoup(html, "html.parser")

    textCategory=[]
    # print(response.text)

    # ----------------------------------------------------
    list=soup.findAll("div", attrs={'class':'attraction_element'})
    print(len(list))

    for el in list:
        site="https://www.tripadvisor.com/"+el.findAll('a')[0]['href']

        nume=el.text.split('\n')[9]
        reviews=el.text.split('\n')[20]
        top=el.text.split('\n')[26]

        # print(nume)
        # print(reviews)
        # print(top)

        element={}
        element["name"]=nume
        element["review"]=reviews
        element["top"]=top
        element["link"]=site

        obiective.append(element)


        # print("___________________")
        # print("___________________")
        # print(el['href'])
    driver.close()


def scrapAllLinks():
    rootLink = "https://www.tripadvisor.com/Attractions-g190454-Activities"
    filterNumber = [(52,1,"Water & Amusement Parks"),(57,3,"Nature & Parks"),(49, 6, "Museums"), (47, 17, "Sights & Landmarks"),(48,1,"Zoos & Aquariums"),
                    (56,5,"Fun & Games"),(20,7,"Nightlife"),(40,3,"Spas & Wellness"),(53,1,"Casinos & Gambling")]

    for filterIt in filterNumber:
        over = 30
        obiective = []
        scrapLinks(rootLink + "-c" + str(filterIt[0]) + "-Vienna.html", obiective)
        for i in range(filterIt[1] - 1):
            scrapLinks(rootLink + "-c" + str(filterIt[0]) + "-oa" + str(over) + "-Vienna.html#FILTERED_LIST", obiective)
            over += 30
        print(len(obiective))
        writeFile(filterIt[2], obiective)


import os
def scrapAllLocation():
    files = []
    filesDone = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk('linksData'):
        for file in f:
            if '.txt' in file:
                files.append(os.path.join(r, file))
    for r, d, f in os.walk('obiectiveData'):
        for file in f:
            if '.txt' in file:
                filesDone.append(os.path.join(r, file))

    print(files)
    print(filesDone)
    for categoryFile in files:
        print("obiectiveData\\"+categoryFile.split('\\')[1])
        if "obiectiveData\\"+categoryFile.split('\\')[1] in filesDone:
            print(categoryFile+" ALREADY TREATED")
        else:
            print(categoryFile)
            f = open(categoryFile, "r")

            obiectiveList=[]
            for x in f:
                x=x.split(';')
                object={}
                object['name']=x[0]
                object['review']=x[1]
                object['top']=x[2]
                object['link']=x[3]
                print("Accessing..")
                try:
                    object['category'],  object['duration'], object['schedule'], object['coordinates'],object['description']=scrapVisitText(object['link'],object['name'])
                    print(object)
                    obiectiveList.append(object)
                except:
                    pass
            print("WRITING\n\n\n\n\n")
            writeLocation(categoryFile.split('\\')[1][:-4], obiectiveList)




def main():
    print("Scrapping links")

    # scrapAllLinks()

    print("Scrapping objectives")

    scrapAllLocation()




main()
