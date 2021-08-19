from selenium import webdriver
from datetime import date
import pandas as pd
from parsers import *

from db_operations import *

#create_table()

target_date = date(2021, 8, 2)

#sources = pd.read_csv('sources.csv')

driver = webdriver.Firefox()

#This does not work
scraper = ECOceansScraper(driver, target_date)

df = scraper.scrape()

print(df)
driver.close()
