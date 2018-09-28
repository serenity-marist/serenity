# Python script to retrieve basic information
# The application will need:
## Selenium webdriver/chromedriver since this is being tested in chrome
## Pandas, numpy, etc.

import pandas as pd
import os
import re
import numpy as np


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask
################# DRIVER CODE PORTION #################
# Executable path ->
app = Flask(__name__)


usernameStr = "khr77"
passwordStr = "master97"



driver = webdriver.Chrome(executable_path='/Users/arielcamilo/downloads/chromedriver')
url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
driver.get(url)



username = driver.find_element_by_id('username')
username.send_keys(usernameStr)

password = driver.find_element_by_id('password')
password.send_keys(passwordStr)

nextButton = driver.find_element_by_css_selector('#welcome > div > div.row.btn-row > input.btn-submit')
nextButton.click()



# driver = webdriver.Chrome(executable_path='/Users/arielcamilo/downloads/chromedriver')
#     #Url to DWORKS
# url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
# driver.get(url)
# delay = 10
#driver.implicity_wait(10)

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

################# STUDENT VIEW SCRAPE #################
studentTable = soup.find("table", attrs={"class": "Inner"})
studentDataTag = studentTable.findAll('td')

studentData = []

for data in studentDataTag:
    #Below one line extracts data
    string = data.decode_contents(formatter="html")
    studentData.append(string)

#studentData
#studentTitle = studentData[::2]
#studentD = studentData[1::2]
#studentTitle
keyVal = dict(zip(studentData[::2], studentData[1::2]))
studentView = pd.DataFrame.from_dict(keyVal, orient='index')
#studentView

filename = 'SerenityStudentInfo.csv'
studentView.to_csv(filename, index=False)
################# BS PORTION TO RETRIEVE HTML FOR BODY #################
