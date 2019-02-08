from Provider import Provider
from urllib import request
import json
import random
import os

class Behance(Provider):
    
    def __init__(self, url):
        super().__init__(url)
        BEHANCE_TOKEN = os.environ["BEHANCE_TOKEN"].strip()
        self.url = "{}{}".format(self.url, BEHANCE_TOKEN)


    def get_popular(self):
        url_request = request.Request(self.url)
        response = request.urlopen(url_request).read()
        shots = json.loads(response.decode("utf-8"))["projects"]
        shot = random.choice(shots)
        shot_url = shot["url"]
        image_url = shot["covers"]["original"]

        return shot_url, image_url