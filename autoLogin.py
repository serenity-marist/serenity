from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

usernameStr = 'khr77'
passwordStr = 'master97'



driver = webdriver.Chrome(executable_path='/Users/arielcamilo/downloads/chromedriver')
url = "https://degreeworks.banner.marist.edu/dashboard/dashboard"
driver.get(url)



username = driver.find_element_by_id('username')
username.send_keys(usernameStr)

password = driver.find_element_by_id('password')
password.send_keys(passwordStr)

nextButton = driver.find_element_by_css_selector('#welcome > div > div.row.btn-row > input.btn-submit')
nextButton.click()
