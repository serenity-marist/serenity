# Python script to retrieve basic information
# The application will need:
## Selenium webdriver/chromedriver since this is being tested in chrome 
## Pandas, numpy, etc.

import pandas as pd 
import os
import re 
import numpy as np
import datetime


from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

################# DRIVER CODE PORTION #################
# Executable path -> 
driver = webdriver.Chrome(executable_path='/Users/alexaj/anaconda3/bin/chromedriver')
    #Url to DWORKS 
url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
driver.get(url)

#driver.implicity_wait(10)
try:
  element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'html > frameset > frame:nth-child(4)'))
  )
finally:
  driver.quit()
################# END DRIVER CODE PORTION #################

################# BS PORTION TO RETRIEVE HTML FOR BODY #################
contFrame = driver.find_element_by_css_selector('html > frameset > frame:nth-child(4)')
driver.switch_to.frame(contFrame)
#frBC = driver.find_element_by_xpath('/html/frameset')
bodyFrame = driver.find_element_by_name('frBody')
driver.switch_to.frame(bodyFrame)

html = driver.page_source
soup = BeautifulSoup(html, "html5lib")
################# END BS PORTION TO RETRIEVE HTML FOR BODY #################

################# GENERAL VARIABLES #################
semYear = datetime.date.today().year
semMonth = datetime.date.today().month
semSsn = ""

if (semMonth >= 1 and semMonth <= 5):
  semSsn = "Spring"
elif (semMonth >= 6 and semMonth <= 8):
  semSsn = "Summer"
elif (semMonth >= 9 and semMonth <= 12):
  semSsn = "Fall"
elif (semMonth = 1):
  semSsn = "Winter"
  
#currSem will be used to indicate current classes
currSem = semSsn + " " + str(semYear)
################# END GEN VARIABLES ###################

################# STUDENT VIEW SCRAPE #################

def studentInfoScrape(soup):
  studentTable = soup.find("table", attrs={"class": "Inner"})
  studentDataTag = studentTable.findAll('td')

  studentData = []

  for stuData in studentDataTag:
      #Below one line extracts data 
      string = stuData.decode_contents(formatter="html")
      studentData.append(string)

  #studentData
  #studentTitle = studentData[::2]
  #studentD = studentData[1::2]
  #studentTitle
  studentKeyVal = dict(zip(studentData[::2], studentData[1::2]))
  studentView = pd.DataFrame.from_dict(studentKeyVal, orient='index')

  studentInfoFile = 'SerenityStudentInfo.csv'
  studentView.to_csv(studenInfoFile, index=False)

################# END STUDENT VIEW SCRAPE #################

##Calling the function to get student info!!
studentInfoScrape(soup)

################# CORE REQ SCRAPE #########################
def coreReqScrape(soup):
  reqStrings = soup.find_all("td", attrs={"class": "RuleLabelTitleNeeded"})

  reqCourses = []
  for reqString in reqStrings:
      req = reqString.decode_contents(formatter="html")
      reqCourses.append(req)

  coreReqs = [x for x in reqCourses if '3 credits' in x]

  coreReqDf = pd.DataFrame(coreReqs)
  coreReqDf.columns = ['Core Requirement']

  coreReqFile = 'SerenityCoreReqs.csv'
  coreReqDf.to_csv(coreReqFile, index=False)
################# END CORE REQ SCRAPE ######################

##Calling the function to get core req info!!
coreReqScrape(soup)

################# MAJO/MIN/DEGREE SCRAPE ###################
def creditProgressScrape(soup):
  headTitle = soup.find_all("td", attrs={"class": "BlockHeadTitle"})
  #subTitle
  headTitleP = []
  for headT in headTitle:
      string = headT.getText()
      headTitleP.append(string)
  #headTitleP

  creditTitles = []
  for headTitle in headTitleP:
      if any(s in headTitle for s in ('Degree', 'Major', 'Minor')):
          creditTitles.append(headTitle)

  subData = soup.find_all("td", attrs={"class": "BlockHeadSubData"})
  #dataNP = array of subData that is not parsed, but converted from obj to str
  subDataNP = []
  for subD in subData:
      string = subD.getText()
      subDataNP.append(string)
      #objToText

  #dataP = array subData that is/will be parsed
  subDataP = []
  for subDataN in subDataNP:
      string = subDataN.split("\xa0 ",1)[1]
      if string:
          subDataP.append(string)
  #subDataP
      
  credits = []

  for subData in subDataP:
      if not any(s in subData for s in ('-', '.')):
          credits.append(subData)

  totalCredits = []
  completedCredits = []
  i = 0
  while i < len(credits):
      if i % 2 == 0:
          totalCredits.append(credits[i])
          i += 1
      else:
          completedCredits.append(credits[i])
          i += 1

  creditsProgress = np.vstack((creditTitles, completedCredits, totalCredits)).T
  creditsProgress = creditsProgress.tolist()
  progressDf = pd.DataFrame(creditsProgress,columns=['Title', 'Credits Completed', 'Total Needed'])
  majMinFile = 'SerenityMajMin.csv'
  progressDf.to_csv(majMinFile, index=False)
################# END MAJO/MIN/DEGREE SCRAPE #############

##Calling the function to get credit progress info!!
creditProgressScrape(soup)

################ DF TO FILES BLOCK ######################
##Unnecessary if I am making functions for each scrape 
################ END DF TO FILES BLOCK ######################
