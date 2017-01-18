# import requests
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GrailedNotify:
    BASE_URL = "https://grailed.com"
    SLEEP_TIME = 1

    def __init__(self, designers, categories, sizes):
        self.designers = designers
        self.categories = categories
        self.sizes = sizes

        self.browser = self.launch()
        self.search()

    # Launches the webdriver
    def launch(self):
        browser = webdriver.Chrome()
        browser.get(self.BASE_URL)
        # Close first time visitor banner
        browser.find_elements_by_css_selector("h1.close")[0].click()
        return browser

    def search(self):
        # Select designers specified in main program
        for designer in self.designers:
            time.sleep(self.SLEEP_TIME)
            search = self.browser.find_elements_by_css_selector("input.search")[1]
            search.clear()
            search.send_keys(designer)
            # Selects indicator for given designer
            time.sleep(self.SLEEP_TIME)
            self.browser.find_elements_by_css_selector("div.indicator")[3].click()

        num_categories = []

        for category in self.categories:
            num_categories.append(self.cat_to_num(category.lower()))

        # Select categories specificed in main program
        for category in num_categories:
            time.sleep(self.SLEEP_TIME)
            self.browser.find_elements_by_css_selector("span.indicator")[category].click()

        # Works sometimes
        # for category in sizes:
        #     if len(category) > 1:
        #         browser.find_elements_by_xpath("//span[contains(text(), '"+ category[0] +"')]")[0].click()
        #         for size in category[1:]:
        #             time.sleep(SLEEP_TIME)
        #             browser.find_elements_by_xpath("//span[contains(text(), '"+ size +"')]")[0].click()

        # Must have a value, minimum can be set to 0 if want no minimum
        # price_min = 100
        # price_max = 300
        #
        # time.sleep(SLEEP_TIME)
        # price = browser.find_elements_by_css_selector("input.price-min")[0]
        # price.clear()
        # price.send_keys(price_min)
        # price = browser.find_elements_by_css_selector("input.price-max")[0]
        # price.clear()
        # price.send_keys(price_max)


    # Converts the category string into an integer
    def cat_to_num(self, category):
        return {
            "tops": 0,
            "bottoms": 1,
            "outerwear": 2,
            "footwear": 3,
            "tailoring": 4,
            "accessories": 5,
        }[category]
