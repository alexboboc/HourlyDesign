from Provider import Provider
from selenium import webdriver
import json, random, os

class Dribbble(Provider):
    
    def __init__(self, url):
        super().__init__(url)
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)


    def get_popular(self):
        # Pick shot
        self.driver.get(self.url)
        elements = self.driver.find_elements_by_class_name("dribbble-over")
        shot = random.choice(elements)
        shot_url = shot.get_attribute("href")
 
        # Extract image url
        self.driver.get(shot_url)
        image = self.driver.find_element_by_css_selector(".main-shot picture source")
        image_url = image.get_attribute("srcset")

        self.driver.quit()
        return shot_url, image_url