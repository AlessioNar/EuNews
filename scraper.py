#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Alessio Nardin
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import bs4
import time


def get_article_list(url, source, driver):

    driver.get(url)

    time.sleep(3)

    if source == 'consigliodeuropait':
        article_containers = driver.find_elements_by_xpath('//div[@class="newsroom "]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    return article_containers


sources = pd.read_csv("sources.csv")
print(sources)

for index, website in sources.iterrows():
    print(website['title'])

link = sources['link'][0]
journal = sources['title'][0]

driver = webdriver.Firefox()

page = get_article_list(link, journal, driver)

driver.close()

soup = bs4.BeautifulSoup(page)

articles = soup.find_all("div", {"class": "element clearfix"})

titles = []
links = []
pub_dates = []
snippets = []
# Testing for consigliodeuropait

for article in articles:
    title = article.h3.text.strip()
    link = article.h3.a['href']
    upper = article.findAll("div", {"class": "upper"})[0]
    if len(upper.findAll("span", {"class":"origine"})) > 0:
        origin = upper.findAll("span", {"class":"origine"})[0]
    else:
        origin = ''
    pub_date = upper.findAll("span", {"class":"date"})[0]
    location = upper.findAll("span", {"class":"location"})[0]
    snippet = article.p.text.strip()
    titles.append(title)
    links.append(link)
    pub_dates.append(pub_date)
    snippets.append(snippet)

print(snippets)

len(snippets)
len(titles)
len(links)
len(pub_dates)


html_source

#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
