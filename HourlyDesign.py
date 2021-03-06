from providers.Dribbble import Dribbble
from providers.Behance import Behance
from providers.FiveHundredPx import FiveHundredPx
from urllib import request
from Poster import Poster
import random, json, os, time

class HourlyDesign:

    def __init__(self):
        self.ENTRYPOINT_BEHANCE = "https://www.behance.net/v2/projects?sort=featured_date&api_key="
        self.ENTRYPOINT_DRIBBBLE = "https://dribbble.com/shots"
        self.ENTRYPOINT_FIVEHUNDREDPX = "https://500px.com/editors/abstract-city+%26+architecture-commercial-fashion-fine+art-performing+arts-uncategorized-urban+exploration"
        self.MAX_IMAGE_SIZE = 5000000

        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context


    def download_image(self, url):
        # Download file and save and save to disk
        file_path = url.split("/")[-1]
        if "." not in file_path:
            file_path = "{}.jpg".format(int(time.time()))
        request.urlretrieve(url, file_path)

        return file_path


    def remove_image(self, path):
        os.remove(path)


    def add_to_history(self, link):
        # Append link at the end of history file
        logline = link + "\n"
        with open("./history.log", "a+") as logfile:
            logfile.write(logline)


    def is_in_history(self, link):
        # No log (first time)
        if not os.path.isfile("./history.log"):
            return False

        # Check if given link is in history file
        with open("./history.log") as logfile:
            history = logfile.readlines()
        
        return str(link) + "\n" in history


    def get_content(self):
        # Pick source and retrieve content from it
        source = None
        n = random.random()
        if n < .33:
            source = Dribbble(self.ENTRYPOINT_DRIBBBLE)
        elif n >= .33 and n < .66:
            source = Behance(self.ENTRYPOINT_BEHANCE)
        else:
            source = FiveHundredPx(self.ENTRYPOINT_FIVEHUNDREDPX)

        url, image = source.get_popular()

        return {
            "source": url,
            "image": image,
            "provider": source.name
        }


    def main(self, retry=5):
        if retry == 0:
            print("Failed five times, terminating")
            exit(1)

        try:
            # Obtain content
            tweet = self.get_content()
            while self.is_in_history(tweet["image"]):
                tweet = self.get_content()
            tweet["imagePath"] = self.download_image(tweet["image"])
            if os.path.getsize(tweet["imagePath"]) > self.MAX_IMAGE_SIZE:
                self.remove_image(tweet["imagePath"])
                raise ValueError("Size bigger than 5MB")

            # Post content
            poster = Poster()
            poster.post_double_tweet(tweet)

            # Cleanup
            self.add_to_history(tweet["image"])
            self.remove_image(tweet["imagePath"])
        except Exception as e:
            print(e)
            self.main(retry=retry - 1)
            

if __name__ == "__main__":
    HourlyDesign().main()
    print("Completed.")