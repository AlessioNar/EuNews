from selenium import webdriver
import time
from websites import *
import pandas as pd

from datetime import date
import dateparser
from transform import standardize_date, std_date_day


source = 'apre'
url = 'https://www.consilium.europa.eu/it/press/press-releases/'
status = 'active'

target_date = date(2021, 7, 19)

driver = webdriver.Firefox()


temp_df = consiglioeuropeo(url, driver, target_date)

temp_df['pub_date'].apply(standardize_date)

temp_df = df
temp_df['source'] = source

temp_df['pub_date'][0]
type(temp_df['pub_date'][0])
type(target_date)
