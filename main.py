import pandas as pd
from navigate import get_article_list
from parse import scrape_articles
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import bs4
import websites


sources = pd.read_csv('sources.csv')
sources = sources.iloc[2].transpose()
for i, source in sources.iterrows():
    if source['website'] == 'apre':
        driver = webdriver.Firefox()
        df = websites.apre(source['link'], driver)
        driver.close()
    elif source['website'] == 'areflh':
        driver = webdriver.Firefox()
        df = websites.areflh(source['link'], driver)
    elif source['website'] = 'consigliodeuropait'
        print(df)

    try:
        if source['status'] == 'active':

            print(source['website'])

            # Getting html page
            html_page = get_article_list(source['link'], source['website'])
            #html_page = get_article_list(url, sources['website'].iloc[0])

            # Parse html
            df = scrape_articles(html_page, source['website'])
            #df = scrape_articles(html_page, sources['website'].iloc[0])
            df_length = len(df.index)

            if df['pub_date'].iloc[df_length - 1] <= start:
                #stop
            else:
                #go on with pagination

            if i != 0:
                df.to_csv('newsletter.csv', mode = 'a', header = False, index = False)
            else:
                df.to_csv('newsletter.csv', mode = 'a', header = True, index = False)
    except:
        print('There has been an error')
