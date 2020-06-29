from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv  
import os


ospath="./outputs"
os.mkdir(ospath)

csvfilename = "./outputs/timesofindia.csv"
error1filename ="./outputs/error1.txt"
error2filename="./outputs/error2.txt"


with open(csvfilename, 'w') as csvfile:       
    csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    csvwriter.writerow(['Headline', 'Date', 'Section', 'Article'])

error1file=open(error1filename,'w') 
error2file=open(error2filename,'w') 

allheadlines=[]
allheadlineslinks=[]
allheadlinesdates=[]
errorsoccured=[]

def getstarttimeval(year, month, date):
    
    monthid=43160
    # monthid=41426
    
    starttimeval=monthid+int(date)-1
    return starttimeval

def getinput():

    year=input("Enter a year: ")
    month=input("Enter month number: ")
    date=input("Enter date: ")

    starttimeval=getstarttimeval(year,month,date)

    getLinksDayAll(year, month, date, starttimeval)

def getLinksDayAll(year,month,date,starttimeval):
     
    driver=webdriver.Firefox()

    linkaddress="https://timesofindia.indiatimes.com/"+str(year)+"/"+str(month)+"/"+str(date)+"/archivelist/year-"+str(year)+",month-"+str(month)+",starttime-"+str(starttimeval)+".cms"
    driver.get(linkaddress)

    headlinelinkslist=driver.find_elements_by_xpath("//span[@style='font-family:arial ;font-size:12;color: #006699']")

    dates={}
    dates['date']=date
    dates['month']=month
    dates['year']=year

    for h in headlinelinkslist:

        source = h.get_attribute('innerHTML')
        html=BeautifulSoup(source, 'html.parser')
        anchor=html('a')
        for an in anchor:

            headlinelink=an.get('href',None)
            headline=an.text
            if headline not in allheadlines:
                allheadlines.append(headline)
                allheadlineslinks.append(headlinelink)
                allheadlinesdates.append(dates)
    
    print("Total number of Headlines:", len(allheadlineslinks))
    if(len(allheadlineslinks) == 0):

        error1file=open(error1filename,'a')
        error1file.write(str(date)+"/"+str(month)+"/"+str(year)+" failed due to connectivity issues\n")
        error1file.close()

    for i in range(len(allheadlineslinks)):

        try:

            pos = [j for j in range(len(allheadlineslinks[i])) if allheadlineslinks[i].startswith("/", j)] 
            section=allheadlineslinks[i][pos[3]+1:pos[4]]
            
            element=driver.get(str(allheadlineslinks[i]))  
                      
            try:
                element=driver.find_element_by_class_name("Normal").text
            except:
                element=driver.find_element_by_class_name("_3WlLe").text

            position=element.find("Download\nThe Times")
            element=element[:position]

            dateformat=str(allheadlinesdates[i]["date"])+"."+str(allheadlinesdates[i]["month"])+"."+str(allheadlinesdates[i]["year"])
            

            rowdata=[]
            rowdata.append(str(allheadlines[i]))
            rowdata.append(str(dateformat))
            rowdata.append(str(section))
            rowdata.append(str(element))

            with open(csvfilename, 'a') as csvfile:       
                csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
                csvwriter.writerow(rowdata)

            print("Article",str(i+1),"fetched")
            
        except:

            error2file=open(error2filename,'a')
            error2file.write(str(allheadlineslinks[i])+"\nDate: "+str(date)+"/"+str(month)+"/"+str(year)+"\n\n")
            error2file.close()
            continue

getinput()