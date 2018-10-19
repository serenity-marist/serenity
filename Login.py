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

################# DRIVER CODE PORTION #################
# Executable path ->

driver = webdriver.Chrome(executable_path=settings.dirpath + '/chromedriver')
    #Url to DWORKS
url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
driver.get(url)


##username and password##
usernameStr = settings.email
passwordStr = settings.password

username = driver.find_element_by_id('username')
username.send_keys(usernameStr)

password = driver.find_element_by_id('password')
password.send_keys(passwordStr)

nextButton = driver.find_element_by_css_selector('#welcome > div > div.row.btn-row > input.btn-submit')
nextButton.click()
