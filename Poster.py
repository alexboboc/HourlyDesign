from twitter import *
import os

class Poster:

    def __init__(self):
        # OAuth initialization for both Twitter accounts
        self.TWITTER_ACCESS = OAuth(
            os.environ["ACCESS_KEY_HD"].strip(),
            os.environ["ACCESS_SECRET_HD"].strip(),
            os.environ["CONSUMER_KEY_HD"].strip(),
            os.environ["CONSUMER_SECRET_HD"].strip()
        )
        self.TWITTER = Twitter(auth=self.TWITTER_ACCESS)
        self.TWITTER_SOURCE_ACCESS = OAuth(
            os.environ["ACCESS_KEY_HDS"].strip(),
            os.environ["ACCESS_SECRET_HDS"].strip(),
            os.environ["CONSUMER_KEY_HDS"].strip(),
            os.environ["CONSUMER_SECRET_HDS"].strip()
        )
        self.TWITTER_SOURCE = Twitter(auth=self.TWITTER_SOURCE_ACCESS)

        # Content support
        self.HASHTAGS = "#design #inspiration #art #creative #artwork"
        self.EMOJI = u'\U0001F48E'


    def post_double_tweet(self, tweet):
        # Upload image to Twitter servers
        with open(tweet["imagePath"], "rb") as file:
            image = file.read()
        uploader = Twitter(domain="upload.twitter.com", auth=self.TWITTER_ACCESS)
        identifier = uploader.media.upload(media=image)["media_id_string"]
        
        # Compute next number
        last_tweet = self.TWITTER.statuses.user_timeline(screen_name="HourlyDesign")[0]["text"]
        last_pearl_number = last_tweet.split()[1]
        pearl_number = int(last_pearl_number) + 1

        # Post main tweet
        mainTweet = "Pearl {} {} (via {}) {}".format(pearl_number, self.EMOJI, tweet["provider"], self.HASHTAGS)
        
        # Post reply with source link
        sourceTweet = "Source: {} @HourlyDesign".format(tweet["source"])
        result = self.TWITTER.statuses.update(status=mainTweet, media_ids=identifier)
        self.TWITTER_SOURCE.statuses.update(status=sourceTweet, in_reply_to_status_id=result["id_str"])