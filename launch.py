from selenium import webdriver
import time
from websites import *
import pandas as pd
from datetime import date
import dateparser
from transform import standardize_date

# Set the target date for article retrieval
target_date = date(2021, 7, 20)

# Set log file
log = open('eunews.log', 'w')
log.close()
dataframe = open('articles.csv', 'w')
dataframe.close()

# Load sources
sources = pd.read_csv('sources.csv')

# Open webdriver
driver = webdriver.Firefox()

# Initialize df
df = pd.DataFrame()

for i, website in sources.iterrows():
    if website['status'] == 'active':
        try:
            temp_df = locals()[website['website']](website['link'], driver, target_date)
            temp_df['source'] = website['website']
            temp_df['section'] = 'Unassigned'
            temp_df = temp_df[temp_df['pub_date'] >= target_date]

            df = df.append(temp_df)
            if len(df) > 0:
                df.to_csv('articles.csv', index = False)
            else:
                print(website['website'] + ' has no new articles')
        except:
            log = open('eunews.log', 'a')
            log.write("There was an error parsing " + website['website'] + '\n')
        time.sleep(5)



driver.close()
