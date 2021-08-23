from selenium import webdriver
from datetime import date
import pandas as pd
from parsers import *
from scraper import Scraper, PaginatedScraper
import time

target_date = date(2021, 8, 16)

driver = webdriver.Firefox()

test = ApreEventScraper(driver, target_date)

test.navigate()
test.preprocess()
test.cookies_removal()
titles, pub_dates, snippets, urls = test.parse()
return self.create_df(titles, pub_dates, snippets, urls)

df = test.scrape()
