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
    if source == 'consiglioeuropeo':
        cookies = driver.find_elements_by_xpath('//span[@id="reject_cookies"]')[0]
        cookies.click()
        article_containers = driver.find_elements_by_xpath('//div[@class="col-md-9 council-flexify-item pull-right"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    return article_containers

sources = pd.read_csv("sources.csv")

link = sources['link'][2]
journal = sources['title'][2]

driver = webdriver.Firefox()

page = get_article_list(link, journal, driver)

driver.close()

soup = bs4.BeautifulSoup(page)

titles = []
links = []
pub_dates = []
snippets = []

# Testing for consiglioeuropeo
list_item = soup.find_all("ul", {"class": "list-group"})
for item in list_item:
    pub_date = item.li.h2.time['datetime']
    article_containers = item.li.ul
    for article in article_containers:
        if type(article) is bs4.element.Tag:
            title = article.div.h3.text
            titles.append(title)
            snippet = article.p.text
            snippets.append(snippet)

print(snippets)


    # Here I have to find all the articles





# Testing for consigliodeuropait
articles = soup.find_all("div", {"class": "element clearfix"})


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

df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
               columns =['title', 'link', 'pub_date', 'snippet'])

print(df)
