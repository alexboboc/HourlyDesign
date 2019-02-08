from Dribbble import Dribbble
from Behance import Behance
from urllib import request
from Poster import Poster
import random, shutil, json, os

class HourlyDesign:

    def __init__(self):
        self.ENTRYPOINT_BEHANCE = "https://www.behance.net/v2/projects?sort=featured_date&api_key="
        self.ENTRYPOINT_DRIBBBLE = "https://dribbble.com/shots"
        self.MAX_IMAGE_SIZE = 5000000


    def download_image(self, url):
        # Download file and save and save to disk
        file_path = url.split("/")[-1]
        with request.urlopen(url) as image, open(file_path, "wb") as file:
            shutil.copyfileobj(image, file)
        
        return file_path


    def remove_image(self, path):
        os.remove(path)


    def add_to_history(self, link):
        # Append link at the end of history file
        logline = link + "\n"
        with open("./files/history.log", "a+") as logfile:
            logfile.write(logline)


    def is_in_history(self, link):
        # No log (first time)
        if not os.path.isfile("./files/history.log"):
            return False

        # Check if given link is in history file
        with open("./files/history.log") as logfile:
            history = logfile.readlines()
        
        return str(link) + "\n" in history


    def read_counter(self):
        # First time
        if not os.path.isfile("./files/counter.txt"):
            return 1

        # Read next post number
        with open("./files/counter.txt") as counterfile:
            counter = int(counterfile.readline().strip())
        counter += 1
        
        return counter


    def increase_counter(self, counter):
        # Save new counter to file
        with open("./files/counter.txt","w") as counterout:
            counterout.write(repr(counter))


    def get_content(self):
        # Pick source and retrieve content from it
        source = None
        n = random.random()
        if n < 0.5:
            source = Dribbble(self.ENTRYPOINT_DRIBBBLE)
        else:
            source = Behance(self.ENTRYPOINT_BEHANCE)

        url, image = source.get_popular()

        return {
            "source": url,
            "image": image
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
            tweet["counter"] = self.read_counter()
            poster = Poster()
            poster.post_double_tweet(tweet)
            self.increase_counter(tweet["counter"])

            # Cleanup
            self.add_to_history(tweet["image"])
            self.remove_image(tweet["imagePath"])
        except Exception as e:
            if tweet:
                self.remove_image(tweet["imagePath"])
            print(e)
            self.main(retry=retry - 1)


if __name__ == "__main__":
    HourlyDesign().main()