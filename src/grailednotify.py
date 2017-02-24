import sqlite3
import time
import yagmail
from sys import platform as _platform
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

class GrailedNotify:
    BASE_URL = "https://grailed.com"
    WAIT_TIME = 1
    SUBJECT = "grailed-notify"
    LOGIN = "grailed.notify@gmail.com"
    PWD = "aykxofzbyhqhbybw"

    def __init__(self, designers, categories, sizes, prices, address, refresh_time=300):
        self.designers = designers
        self.categories = categories
        self.sizes = sizes
        self.prices = prices
        self.address = address
        self.refresh_time = refresh_time

        print "Welcome to grailed-notify, please be patient as everything is set up"

        self.email = self.connect()
        self.browser = self.launch()
        self.search_url = self.search()

        # Creates listings table in database if it does not exist
        db = sqlite3.connect("./src/Listings.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS listings (link TEXT PRIMARY KEY, price NUM)")
        db.commit()
        db.close()

        self.listings = []
        # self.duplicates = []

    def __del__(self):
        self.browser.close()

    # Connect to e-mail account
    def connect(self):
        email = yagmail.SMTP(self.LOGIN, self.PWD)
        print "Connecting to e-mail server... ",
        print "Done"
        return email

    # Launches the webdriver
    def launch(self):
        print "Launching " + self.BASE_URL + "... ",

        # Decide which binary file to use based on user OS
        if _platform == "linux" or _platform == "linux2":
           binary_file = "-linux"
        elif _platform == "darwin":
           binary_file = "-mac"
        elif _platform == "win32":
           binary_file = ".exe"

        browser = webdriver.Chrome("./bin/chromedriver" + binary_file)
        browser.set_window_size(1200, 600)
        browser.get(self.BASE_URL)

        # Tries to close the first time visitor banner if present
        try:
            browser.find_elements_by_css_selector("h1.close")[0].click()
            print "Done"
        except WebDriverException:
            print "ERROR: First time visitor banner not present"

        return browser

    # Searches Grailed using given filters
    def search(self):
        print "Searching Grailed with given filters... ",
        time.sleep(self.WAIT_TIME)

        # Select designers specified
        for designer in self.designers:
            search = self.browser.find_elements_by_css_selector("input.search")[1]
            time.sleep(self.WAIT_TIME)
            search.clear()
            search.send_keys(designer)

            xpath = "//div//div//div//div//div//div//div//div//div//div//div//div//div"
            time.sleep(self.WAIT_TIME)
            designer_indicator = self.browser.find_elements_by_xpath(xpath)[0]
            self.click(designer_indicator)

        # Convert categories to numeric values
        num_categories = []
        for category in self.categories:
            num_categories.append(self.cat_to_num(category.lower()))

        # Select categories specified
        for category in num_categories:
            time.sleep(self.WAIT_TIME)
            category_indicator = self.browser.find_elements_by_css_selector("span.indicator")[category]
            self.click(category_indicator)

        # Select sizes specified
        for category in self.sizes:
            # Only open size categories that have more than one element
            if len(category) > 1:
                time.sleep(self.WAIT_TIME)
                category_dropdown = self.browser.find_elements_by_xpath("//span[contains(text(), '" + category[0] + "')]")[0]
                self.click(category_dropdown)

                # Click sizes
                for size in category[1:]:
                    time.sleep(self.WAIT_TIME)
                    size_box = self.browser.find_elements_by_xpath("//span[contains(text(), '" + size + "')]")[0]
                    self.click(size_box)

                # Close the size category
                time.sleep(self.WAIT_TIME)
                self.click(category_dropdown)

        price_min = self.prices[0]
        price_max = self.prices[1]

        # Input the minimum and maximum price
        time.sleep(self.WAIT_TIME)
        price = self.browser.find_elements_by_css_selector("input.price-min")[0]
        price.clear()
        price.send_keys(price_min)
        price = self.browser.find_elements_by_css_selector("input.price-max")[0]
        price.clear()
        price.send_keys(price_max)

        print "Done"
        time.sleep(self.WAIT_TIME)
        search_url = self.browser.current_url
        return search_url

    # Tries to click the given element a first time, clicks again if first doesn't
    # work, as this solves 99% of click errors
    def click(self, element):
        try:
            element.click()
        except WebDriverException:
            element.click()

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

    # Refresh the listings
    # Perhaps make this hit 'RELOAD' instead, and get new URL
    def refresh(self):
        print "Refrehsing page " + self.search_url + "... ",
        self.browser.get(self.search_url)
        print "Done"

    # Retrieves listings for all listings
    def scrape(self):
        time.sleep(self.WAIT_TIME)
        xpath = "//div//div//div//div//div//div//div//div//div//div//"
        links = self.browser.find_elements_by_xpath(xpath + "a[@href]")
        num_links = len(links)

        for i in range(num_links):
            self.listings.append(links[i].get_attribute("href"))

    # Notifies user with new link if not a duplicate
    def notify(self):
        subject = self.SUBJECT + " " + time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S")
        content = ""

        # Create body of e-mail
        for listing in self.listings:
            if self.duplicate(listing) != True:
                content += listing + "\n"

        # Send the e-mail if it has content
        print "Sending listings to " + self.address + "...",
        if(content != ""):
            content = "These listings met your filters:\n" + content
            self.email.send(self.address, subject, [content])
            print "Done"
        else:
            print "ERROR: No new listings to send"

    # Check if the link is a duplicate
    def duplicate(self, link):
        duplicate_flag = False

        db = sqlite3.connect("./src/Listings.db")
        c = db.cursor()
        c.execute("SELECT link FROM listings WHERE link=?", (link,))
        results = c.fetchall()

        # If listings is not a duplicate, add it to the database
        if not results:
            # CHANGE 0 TO PRICE
            self.insert_listing(link, 0)
        # If listings is a duplicate, check if priced has decreased
        else:
            duplicate_flag = True

        db.commit()
        db.close()
        return duplicate_flag

    def insert_listing(self, link, price):
        db = sqlite3.connect("./src/Listings.db")
        c = db.cursor()
        c.execute("INSERT INTO listings VALUES (?, ?)", (link, price))
        db.commit()
        db.close()


    # Frees up list of listings
    def del_links(self):
        del self.listings[:]

    # Main loop
    def main(self):
        while True:
            # Must reload before scraping due to bug on Grailed creating duplicate listings
            self.refresh()
            self.scrape()
            self.notify()
            # self.populate_duplicates()
            self.del_links()
            print "Sleeping for " + `self.refresh_time` + " seconds..."
            time.sleep(self.refresh_time)
