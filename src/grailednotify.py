# import requests
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GrailedNotify:
    BASE_URL = "https://grailed.com"
    SLEEP_TIME = 1

    def __init__(self, designers, categories, sizes, prices):
        self.designers = designers
        self.categories = categories
        self.sizes = sizes
        self.prices = prices

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

        # Convert categories to numeric values
        categories = []
        for category in self.categories:
            categories.append(self.cat_to_num(category.lower()))

        # Select categories specificed in main program
        for category in categories:
            time.sleep(self.SLEEP_TIME)
            self.browser.find_elements_by_css_selector("span.indicator")[category].click()

        # Select sizes specificed in main program
        for category in self.sizes:
            if len(category) > 1:
                self.browser.find_elements_by_xpath("//span[contains(text(), '" + category[0] + "')]")[0].click()
                for size in category[1:]:
                    time.sleep(self.SLEEP_TIME)
                    self.browser.find_elements_by_xpath("//span[contains(text(), '" + size + "')]")[0].click()

        # price_min = self.prices[0]
        # price_max = self.prices[1]

        # time.sleep(self.SLEEP_TIME)
        # price = self.browser.find_elements_by_css_selector("input.price-min")[0]
        # price.clear()
        # price.send_keys(price_min)
        # price = self.browser.find_elements_by_css_selector("input.price-max")[0]
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
