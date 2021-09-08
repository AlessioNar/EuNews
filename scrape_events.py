from selenium import webdriver
from datetime import date
import pandas as pd
from parsers import *

from db_operations import *

#create_table()

target_date = date(2021, 8, 17)

sources = pd.read_csv('event_sources.csv')
sources = sources.loc[sources['status'] == 'active']

driver = webdriver.Firefox()
final_df = pd.DataFrame()

for index, website in sources.iterrows():
    print(website['website'])
    if website['website'] == 'apre_eventi':
        scraper = ApreEventScraper(driver, target_date)
    elif website['website'] == 'cor_events':
        scraper = COREventScraper(driver, target_date)
    elif website['website'] == 'earlall_eventi':
        scraper = EarlAllEventScraper(driver, target_date)
    elif website['website'] == 'eib_eventi':
        scraper = EIBEventScraper(driver, target_date)
    elif website['website'] == 'eit_eventi':
        scraper = EITEventScraper(driver, target_date)
    elif website['website'] == 'interreg_eventi':
        scraper = InterregEventScraper(driver, target_date)
    elif website['website'] == 'jrc_eventi':
        scraper = JRCEventScraper(driver, target_date)
    else:
        pass

    df = scraper.scrape()
    final_df = final_df.append(df)
    # Here i need to put the source
    #for id, article in df.iterrows():
    #    try:
    #        insert_articles(article['title'], article['pub_date'].strftime("%Y-%m-%d"), article['snippet'], article['url'], website['website'])
    #    except:
    #        insert_articles(article['title'], date(2021,12,31).strftime("%Y-%m-%d"), article['snippet'], article['url'], website['website'])

final_df.to_csv("test.csv", index=False)
driver.close()
