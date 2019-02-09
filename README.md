# HourlyDesign Twitter Bot

HourlyDesign is a **[Twitter bot]() that tweets bits of graphic inspiration every 60 minutes**. To do so, it accesses several websites (`Providers`, in the application) either through APIs or scraping them, and it extracts popular content.

For reference, I wrote a [blog post](http://blog.alexboboc.com/twitter-bot-selenium-scraping-design/) on the idea, design and implementation decisions behind the project.

## Technologies

- The project is written in **Python 3**.
- For scraping, [**Selenium for Python**](http://selenium-python.readthedocs.io/)  is used.
- Selenium requires the last versions of **ChromeDriver** and **Google Chrome** in the system, which are installed running the provided `setup.sh` script.
- The Twitter API is accessed through the twitter [**python package**](https://pypi.org/project/twitter/).

## Active providers

At the moment, the following providers are active:

- [Behance](https://behance.com) - accessed through API.
- [Dribbble](https://dribbble.com) - scraped with Selenium.

There are plans to extend this list adding DeviantArt, ArtStation and similar.

## Run

The entrypoint of the project is `HourlyDesign.py`.

While running the project is easy, it requires a total of 9 environment variables to be set:

- `ACCESS_KEY_HD`, `ACCESS_SECRET_HD`, `CONSUMER_KEY_HD` and `CONSUMER_SECRET` for the main Twitter account.
- `ACCESS_KEY_HDS`, `ACCESS_SECRET_HDS`, `CONSUMER_KEY_HDS` and `CONSUMER_SECRETS` for a second Twitter account posts sources as replies to the original tweets.
- `BEHANCE_TOKEN` to authenticate requests to the Behance API.