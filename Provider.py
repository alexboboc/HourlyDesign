class Provider:

    def __init__(self, url):
        self.url = url
        self.INTERACTION_SLEEP_TIME = 3

    def get_pupular(self):
        print("[ERROR] Method get_popular not implemented in subclass.")
        exit(1)