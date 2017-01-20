import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GrailedNotify:
    BASE_URL = "https://grailed.com"
    WAIT_TIME = 1
    REFRESH_TIME = 30

    def __init__(self, designers, categories, sizes, prices):
        self.designers = designers
        self.categories = categories
        self.sizes = sizes
        self.prices = prices

        self.browser = self.launch()
        self.search_url = ""
        self.links = []
        self.duplicates = []

    def __del__(self):
        self.browser.close()

    # Launches the webdriver
    def launch(self):
        # browser = webdriver.PhantomJS()
        browser = webdriver.Chrome()
        browser.set_window_size(1200, 600)
        browser.get(self.BASE_URL)

        # Tries to close the first time visitor banner if present
        try:
            browser.find_elements_by_css_selector("h1.close")[0].click()
        except Exception:
            print "Error: First time visitor banner not present"

        return browser

    # Searches Grailed using given filters
    def search(self):
        time.sleep(self.WAIT_TIME)
        
        # Select designers specified in main program
        for designer in self.designers:
            search = self.browser.find_elements_by_css_selector("input.search")[1]
            search.clear()
            search.send_keys(designer)
            # Selects indicator for given designer
            time.sleep(self.WAIT_TIME)
            self.browser.find_elements_by_css_selector("div.indicator")[3].click()

        # Convert categories to numeric values
        num_categories = []
        for category in self.categories:
            num_categories.append(self.cat_to_num(category.lower()))

        for category in num_categories:
            time.sleep(self.WAIT_TIME)
            self.browser.find_elements_by_css_selector("span.indicator")[category].click()

        for category in self.sizes:
            # Only open size categories that have more than one element
            if len(category) > 1:
                # First click of category often fails, but always works on second try
                try:
                    self.browser.find_elements_by_xpath("//span[contains(text(), '" + category[0] + "')]")[0].click()
                except Exception:
                    print "Error: First click failed, trying again"
                    self.browser.find_elements_by_xpath("//span[contains(text(), '" + category[0] + "')]")[0].click()
                # Select sizes
                for size in category[1:]:
                    time.sleep(self.WAIT_TIME)
                    self.browser.find_elements_by_xpath("//span[contains(text(), '" + size + "')]")[0].click()
                # Close the category
                time.sleep(self.WAIT_TIME)
                self.browser.find_elements_by_xpath("//span[contains(text(), '" + category[0] + "')]")[0].click()

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

        time.sleep(self.WAIT_TIME)
        self.search_url = self.browser.current_url

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

    # Retrieves links for all listings
    def scrape(self):
        time.sleep(self.WAIT_TIME)
        xpath = "//div//div//div//div//div//div//div//div//div//div//"
        listings = self.browser.find_elements_by_xpath(xpath + "a[@href]")
        num_listings = len(listings)

        for i in range(num_listings):
            self.links.append(listings[i].get_attribute("href"))

    # Populate the duplicates list for later use
    def populate_duplicates(self):
        for link in self.links:
            if self.duplicate(link) != True:
                self.duplicates.append(link)

    # Frees up list of links
    def del_links(self):
        del self.links[:]

    # Notifies user with new link if not a duplicate
    def notify(self):
        for link in self.links:
            if self.duplicate(link) != True:
                print link

    # Check if the link is a duplicate
    def duplicate(self, link):
        if self.duplicates.count(link) == 0:
            return False
        return True

    # Refresh the listings
    def refresh(self):
        self.browser.get(self.search_url)

    # Main loop
    def loop(self):
        self.search()
        while True:
            # Must reload before scraping due to bug on Grailed creating duplicate listings
            self.refresh()
            self.scrape()
            self.notify()
            self.populate_duplicates()
            self.del_links()
            time.sleep(self.REFRESH_TIME)
