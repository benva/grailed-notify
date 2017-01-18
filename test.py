import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
BASE_URL = "https://grailed.com"
browser = webdriver.Chrome()
browser.get(BASE_URL)
browser.find_elements_by_css_selector("h1.close")[0].click()
