# Python script to retrieve basic information
# The application will need:
## Selenium webdriver/chromedriver since this is being tested in chrome 
## Pandas, numpy, etc.

import pandas as pd 
import os
import re 
import numpy as np
import datetime
import sys 

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


##username and password##
usernameStr = "xx@marist.edu"
passwordStr = "xx"

username = driver.find_element_by_id('username')
username.send_keys(usernameStr)

password = driver.find_element_by_id('password')
password.send_keys(passwordStr)

nextButton = driver.find_element_by_css_selector('#welcome > div > div.row.btn-row > input.btn-submit')
nextButton.click()
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
headTitles = soup.find_all("td", attrs={"class": "BlockHeadTitle"})
headTitle = []
for head in headTitles:
    headTitle.append(head.text)
#Students info: 
#arrays: major(s), minor(s), degree
#strings: pway (since there can only be one)
degreeName = [x for x in headTitle if 'Degree' in x]
concentrations = [x for x in headTitle if 'Concentration' in x]
majorArray = [x for x in headTitle if 'Major' in x]
minorArray = [x for x in headTitle if 'Minor' in x]
pwayName = [x for x in headTitle if 'Pathway' in x][0]

semYear = datetime.date.today().year
semMonth = datetime.date.today().month
semSsn = ""

if (semMonth > 1 and semMonth <= 5):
  semSsn = "Spring"
elif (semMonth >= 6 and semMonth <= 8):
  semSsn = "Summer"
elif (semMonth >= 9 and semMonth <= 12):
  semSsn = "Fall"
elif (semMonth == 1):
  semSsn = "Winter"

#currSem will be used to indicate current classes
currSem = semSsn + " " + str(semYear)
################# END GEN VARIABLES ###################

################# STUDENT VIEW SCRAPE #################

def studentInfoScrape(soup):
  studentTable = soup.find("table", attrs={"class": "Inner"})

  studentInfoDf = pd.read_html(str(studentTable))[0]

  primValue = list(studentInfoDf[0])
  primInfo = list(studentInfoDf[1])
  secondColumn = list(studentInfoDf[2])
  thirdColumn = list(studentInfoDf[3])

  finalValue = primValue + secondColumn
  finalInfo = primInfo + thirdColumn

  studentInfo = np.vstack((finalValue, finalInfo)).T
  studentInfo = studentInfo.tolist()

  studentInfoFinalDf = pd.DataFrame(studentInfo,columns=['Values', 'Infor'])
  #studentInfoFinalDf

  studentInfoFileJSON = 'SerenityStudentInfo.json'
  studentInfoFinalDf.to_json(studentInfoFileJSON, orient='records')

################# END STUDENT VIEW SCRAPE #################

##Calling the function to get student info!!
studentInfoScrape(soup)

################# CORE REQ SCRAPE #########################
def coreReqScrape(soup):
  reqStrings = soup.find_all("td", attrs={"class": "RuleLabelTitleNeeded"})

  reqCourses = []
  for reqString in reqStrings:
    reqCourses.append(reqString.text)

  coreReqs = [x for x in reqCourses if '3 credits' in x]

  coreReqDf = pd.DataFrame(coreReqs)
  coreReqDf.columns = ['Core Requirement']

  #JSON of DataFrame is default, CSV commented out
  # coreReqFileCSV = 'SerenityCoreReqs.csv'
  # coreReqDf.to_csv(coreReqFileCSV, index=False)
  coreReqFileJSON = 'SerenityCoreReqs.json'
  coreReqDf.to_json(coreReqFileJSON, orient='records')
################# END CORE REQ SCRAPE ######################

##Calling the function to get core req info!!
coreReqScrape(soup)

################# MAJO/MIN/DEGREE SCRAPE ###################
def creditProgressScrape(soup):
  creditTitles = []
  creditTitles = degreeName + majorArray + minorArray

  subData = soup.find_all("td", attrs={"class": "BlockHeadSubData"})
  #dataNP = array of subData that is not parsed, but converted from obj to str
  subDataNP = []
  for subD in subData:
    subDataNP.append(subD.text)
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
  
  creditTitles = []
  creditTitles = degreeName + majorArray + concentrations + minorArray 
  if (len(creditTitles) * 2 != len(credits)):
    creditTitles = degreeName + concentrations + minorArray 

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
  
  #JSON of DataFrame is default, CSV commented out
  # majMinFileCSV = 'SerenityMajMin.csv'
  # progressDf.to_csv(majMinFileCSV, index=False)
  majMinFileJSON = 'SerenityMajMin.json'
  progressDf.to_json(majMinFileJSON, orient='records')
################# END MAJO/MIN/DEGREE SCRAPE #############

##Calling the function to get credit progress info!!
creditProgressScrape(soup)

################# CURRENT CLASSES SCRAPE ##################
def currClassScrape(soup):
  currClassHTML = soup.find_all("table", attrs={"class": "xBlocks"})

  if(len(currClassHTML) > 2):
      currClassHTML = currClassHTML[2]
  else:
      currClassHTML = currClassHTML[1]
  
  #classNames
  className = currClassHTML.find_all("td", attrs={"class": "SectionCourseTitle"})
  classNames = []

  for classes in className:
      classNames.append(classes.text)
      
  #classNumbers
  classNo = currClassHTML.find_all("td", attrs={"class": "ClassesAppliedClasses"})
  classNos = []

  for no in classNo:
      no = no.text.replace(u'\xa0', u' ')
      classNos.append(no)

  #creditsEach
  noCredits = currClassHTML.find_all("td", attrs={"class": "SectionCourseCredits"})
  curCredits = []

  for noCreds in noCredits:
      curCredits.append(noCreds.text)
  
  currClassDataStack = np.vstack((classNos, classNames, curCredits)).T
  currClassDataStack = currClassDataStack.tolist()

  currClassInfoDf = pd.DataFrame(currClassDataStack,columns=['Course No', 'Course Title', 'Credit Value'])
  
  #JSON of DataFrame is default, CSV commented out
  # currClassFileCSV = 'SerenityCurrClass.csv'
  # currClassInfoDf.to_csv(currClassFileCSV, index=False)
  currClassFileJSON = 'SerenityCurrClass.json'
  currClassInfoDf.to_json(currClassFileJSON, orient='records')
################# END CURR CLASSES SCRAPE ##################

##Calling the function to get curr class info!!
currClassScrape(soup)

###################### PATHWAY SCRAPE ######################
def pathwayScrape(soup):
  pathwayClassesDri = driver.find_element_by_css_selector('#frmAudit > table:nth-child(28) > tbody > tr > td > table > tbody > tr:nth-child(5) > td.RuleLabelData > table')
  pathwaySoup = BeautifulSoup(pathwayClassesDri.get_attribute('innerHTML'), "html5lib")

  pathwayTable = pathwaySoup.find_all('table')[0]
  pathwayDf = pd.read_html(str(pathwayTable))[0]
  pathwayDf.columns = ['Course No', 'Course Title', 'Grade', 'Credits', 'Semester']

  #JSON of DataFrame is default, CSV commented out
  pathwayFileJSON = 'SerenityPathway.json'
  pathwayDf.to_json(pathwayFileJSON, orient='records')
  # pathwayFileCSV = 'SerenityPathway.csv'
  # pathwayDf.to_json(pathwayFileCSV, index=False)

###################### END PWAY SCRAPE ######################

##Calling the function to get pathway  info!!
pathwayScrape(soup)

################ CLOSE SESSION ######################

#closes the driver session safely 
#driver.dispose()

################ END SCRAPE PYTHON ######################
