from Provider import Provider
from selenium import webdriver
import json, random, os, time

class FiveHundredPx(Provider):
    
    def __init__(self, url):
        super().__init__(url, "500px")
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)


    def get_popular(self):
        # Pick photo
        self.driver.get(self.url)
        time.sleep(self.INTERACTION_SLEEP_TIME)
        photos = self.driver.find_elements_by_css_selector("a.photo_link")
        photo = random.choice(photos)
        photo_url = photo.get_attribute("href")
 
        # Extract image url
        self.driver.get(photo_url)
        time.sleep(self.INTERACTION_SLEEP_TIME)
        photo_element = self.driver.find_element_by_css_selector(".photo-show__img")
        photo_src = photo_element.get_attribute("src")

        self.driver.quit()
        return photo_url, photo_src