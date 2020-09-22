# web_scraper
A casual web scraper for a girl named Sarah

## Requirements

This project is written in python 3.6. Install the additional requirements using the `requirements.txt`: 

* (recommended) Create a python virtual environment
  * Create the venv: `python3 -m venv .venv`
  * Activate the environment: `source .venv/bin/activate`
* Install requirements
  * `python3 -m pip install -r requirements.txt --user`


## Scraping Stuff

This project uses the `scrapy` library to implement basic web-scraping functionality. In order to run the spider and parse the set website, run the following command:

`scrapy runspider scraper.py`