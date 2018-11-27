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
import settings
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

################# DRIVER CODE PORTION #################
# Executable path ->


    #Url to DWORKS



##username and password##
def logout():
  settings.driver.quit()

def login():
  settings.driver = webdriver.Remote("http://10.11.12.22:4444/wd/hub", DesiredCapabilities.CHROME)

  url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
  settings.driver.get(url)
  usernameStr = settings.email
  passwordStr = settings.password

  username = settings.driver.find_element_by_id('username')
  username.send_keys(usernameStr)

  password = settings.driver.find_element_by_id('password')
  password.send_keys(passwordStr)

  nextButton = settings.driver.find_element_by_css_selector('#welcome > div > div.row.btn-row > input.btn-submit')
  nextButton.click()
  isCheckable = settings.driver.find_element_by_css_selector('html > frameset > frame:nth-child(4)')
################# END DRIVER CODE PORTION #################
def runScrape():
  print(settings.email)
  ################# BS PORTION TO RETRIEVE HTML FOR BODY #################
  contFrame = settings.driver.find_element_by_css_selector('html > frameset > frame:nth-child(4)')
  settings.driver.switch_to.frame(contFrame)
  #frBC = driver.find_element_by_xpath('/html/frameset')
  bodyFrame = settings.driver.find_element_by_name('frBody')
  settings.driver.switch_to.frame(bodyFrame)

  html = settings.driver.page_source
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

  settings.jsonObjects = []
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

    finalValue = primValue + secondColumn # resulting array
    finalInfo = primInfo + thirdColumn    # resulting array
    finalInfo = [x for x in finalInfo if str(x) != 'nan']
    finalValue = [x for x in finalValue if str(x) != 'nan']
    #Vstacked dataframe if converted to a json file
      # studentInfo = np.vstack((finalValue, finalInfo)).T
      # studentInfo = studentInfo.tolist()

      # studentInfoFinalDf = pd.DataFrame(studentInfo,columns=['Values', 'Infor'])
      #studentInfoFinalDf

      # studentInfoFileJSON = 'SerenityStudentInfo.json'
    studentDict = dict(zip(finalValue, finalInfo))

    if 'Advisors' in studentDict:
      studentDict['Advisor'] = studentDict['Advisors']
      del studentDict['Advisors']

    if 'Majors' in studentDict:
      studentDict['Major'] = studentDict['Majors']
      del studentDict['Majors']
  
    if 'Minors' in studentDict:
      studentDict['Minor'] = studentDict['Minors']
      del studentDict['Minors']

    return studentDict

  ################# END STUDENT VIEW SCRAPE #################

  ##Calling the function to get student info!!
  settings.jsonObjects.append(studentInfoScrape(soup))

  ################# CORE REQ SCRAPE #########################
  def coreReqScrape(soup):
    reqStrings = soup.find_all("td", attrs={"class": "RuleLabelTitleNeeded"})

    reqCourses = []
    for reqString in reqStrings:
      reqCourses.append(reqString.text)

    coreReqs = [x for x in reqCourses if '3 credits' in x] #Resulting array

    if not coreReqs: #Exception handler
      return
    else:
      coreRTitle = []
      for x in coreReqs:
          coreRTitle.append("Core Class Required")
      coreDict = dict(zip(coreRTitle, coreReqs))
      # coreDict = json.dumps(coreDict)

    return coreDict
    # return coreReqJSON
  ################# END CORE REQ SCRAPE ######################

  ##Calling the function to get core req info!!
  # settings.jsonObjects.append(coreReqScrape(soup))

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

    #Resulting array is totalCredits and completedCredits, block should be here
    creditsProgress = np.vstack((creditTitles, completedCredits, totalCredits)).T
    creditsProgress = creditsProgress.tolist()
    progressDf = pd.DataFrame(creditsProgress,columns=['title', 'completedCredits', 'totalNeeded'])

    #JSON of DataFrame is default, CSV commented out
    # majMinFileCSV = 'SerenityMajMin.csv'
    # progressDf.to_csv(majMinFileCSV, index=False)
    # majMinFileJSON = 'SerenityMajMin.json'
    progressJSON = progressDf.to_dict(orient='records')
    return progressJSON
  ################# END MAJO/MIN/DEGREE SCRAPE #############

  ##Calling the function to get credit progress info!!
  progressFinalJSON = creditProgressScrape(soup)
  arr = []
  for x in progressFinalJSON:
    # x = json.dumps(x)
    arr.append(x)
  settings.jsonObjects.append(arr)

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
    currClassDataStack = currClassDataStack.tolist() #Resulting array

    currClassInfoDf = pd.DataFrame(currClassDataStack,columns=['currCourseNum', 'currCourseTitle', 'currCreditValue'])

    #JSON of DataFrame is default, CSV commented out
    # currClassFileCSV = 'SerenityCurrClass.csv'
    # currClassInfoDf.to_csv(currClassFileCSV, index=False)
    # currClassFileJSON = 'SerenityCurrClass.json'
    currClassJSON = currClassInfoDf.to_dict(orient='records')

    return currClassJSON
  ################# END CURR CLASSES SCRAPE ##################

  ##Calling the function to get curr class info!!
  currClassFinalJSON = currClassScrape(soup)
  arr = []
  for x in currClassFinalJSON:
    # x = json.dumps(x)
    arr.append(x)
  settings.jsonObjects.append(arr)

  ###################### PATHWAY SCRAPE ######################
  def pathwayScrape(soup):
    pathwayClassesDri = settings.driver.find_element_by_css_selector('#frmAudit > table:nth-child(28) > tbody > tr > td > table > tbody > tr:nth-child(5) > td.RuleLabelData > table')
    pathwaySoup = BeautifulSoup(pathwayClassesDri.get_attribute('innerHTML'), "html5lib")

    #In this case the exception might be different. Check if functionality for checking empty table
    pathwayTable = pathwaySoup.find_all('table')[0]
    pathwayDf = pd.read_html(str(pathwayTable))[0]

    pathwayDf.columns = ['pathwayNum', 'pathwayTitle', 'pathwayGrade', 'pathwayCred', 'pathwayYear']

    pathwayJSON = pathwayDf.to_dict(orient="records")

    #JSON of DataFrame is default, CSV commented out
    # pathwayFileJSON = 'SerenityPathway.json'
    # pathwayJSON = pathwayDf.to_json(orient='records')
    return pathwayJSON

  ###################### END PWAY SCRAPE ######################

  # Calling the function to get pathway  info!!
  finalPathwayJSON = pathwayScrape(soup)
  arr = []
  for x in finalPathwayJSON:
    # x = json.dumps(x)
    arr.append(x)
  settings.jsonObjects.append(arr)

################ CLOSE SESSION ######################

#closes the driver session safely
#

################ END SCRAPE PYTHON ######################
