from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from websites import *
import pandas as pd
from datetime import date

# Set the target date for article retrieval
date = date(2021, 7, 19)

# Set log file
log = open('eunews.log', 'w')
log.close()

# Load sources
sources = pd.read_csv('sources.csv')

# Open webdriver
driver = webdriver.Firefox()
df = pd.DataFrame()
for i, website in sources.iterrows():
    try:
        temp_df = locals()[website['website']](website['link'], driver, date)
        df = df.append(temp_df)
        df = df[df['pub_date'] >= date]
        df.to_csv('articles.csv')
    except:
        log = open('eunews.log', 'a')
        log.write("There was an error parsing " + website['website'] + '\n')

    time.sleep(3)

driver.close()
