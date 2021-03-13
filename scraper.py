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
    if source == 'eucommission':
        article_containers = driver.find_elements_by_xpath('//section[@id="news-block"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    if source == 'consiglioeuropeo':
        cookies = driver.find_elements_by_xpath('//span[@id="reject_cookies"]')[0]
        cookies.click()
        article_containers = driver.find_elements_by_xpath('//div[@class="col-md-9 council-flexify-item pull-right"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    if source == 'esma':
        article_containers = driver.find_elements_by_xpath('//table[@class="views-view-grid cols-2"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    return article_containers

sources = pd.read_csv("sources.csv")

link = sources['link'][3]
journal = sources['title'][3]

driver = webdriver.Firefox()

page = get_article_list(link, journal, driver)

driver.close()

soup = bs4.BeautifulSoup(page)

titles = []
links = []
pub_dates = []
snippets = []

# Testing for consiglioeuropeo
list_item = soup.section.ul.find_all("div", {"_ngcontent-c1": ""})

for item in list_item:
    article = item.li
    if type(article) is bs4.element.Tag:
        category = item.div.div.span.text
        pub_date = item.div.div.find_all("span", {"ngcontent-c1":""})[1].text
        link = article.a['href']
        if type(item.div.h3) is bs4.element.Tag:
            title = item.div.h3.text
        else:
            title = ''
        if type(item.div.p) is bs4.element.Tag:
            snippet = item.div.p.text
        else:
            snippet = ''
        titles.append(title)
        pub_dates.append(pub_date)
        links.append(link)
        snippets.append(snippet)


df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
               columns =['title', 'link', 'pub_date','snippet'])

print(df)

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
            link = article.div.h3.a['href']
            snippet = article.p.text
            links.append(link)
            titles.append(title)
            snippets.append(snippet)
            pub_dates.append(pub_date)

df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
               columns =['title', 'link', 'pub_date','snippet'])

print(df)


len(links)
len(titles)
len(snippets)
len(article_containers)
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

# test esma

# Here the articles are structured in rows/columns
rows = soup.find_all("tr")
for row in rows:
    cols = row.find_all("td")
    for col in cols:
        title = col.h2.a.text
        link = col.h2.a['href']
        pub_date = col.find_all("div", class_="field field-type-ds")[0].text.strip()
        snippet = col.find_all("div", class_="news_cartouche-text")[0].text.strip()
        titles.append(title)
        links.append(link)
        pub_dates.append(pub_date)
        snippets.append(snippet)

df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
               columns =['title', 'link', 'pub_date', 'snippet'])

print(df)
