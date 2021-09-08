from selenium import webdriver
from datetime import date
import pandas as pd
from scraper import Scraper, PaginatedScraper, EventScraper
from parsers import *

import time

target_date = date(2021, 8, 30)

driver = webdriver.Firefox()

test = ECEducationEventScraper(driver, target_date)

test.navigate()
test.preprocess()
test.cookies_removal()
#soup = test.extract_html()
#list_item = soup.find_all('article')

titles, snippets, start_dates, end_dates, urls = test.parse()
test.create_df(titles, start_dates, end_dates, snippets, urls)

df = test.scrape()
