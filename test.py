from selenium import webdriver
import time
from websites import *
import pandas as pd

from datetime import date
import dateparser
from transform import standardize_date, std_date_day


source = 'enicbcmed'
url = 'https://www.eif.org/news_centre/press_releases/all/index.htm?year=0000&category=&keywordList='
status = 'active'

target_date = date(2021, 7, 20)

driver = webdriver.Firefox()

temp_df = eif(url, driver, target_date)

temp_df['pub_date'].apply(standardize_date)

temp_df = df
temp_df['source'] = source

temp_df['pub_date'][0]
type(temp_df['pub_date'][0])
type(target_date)
