#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Alessio Nardin
"""

import pandas as pd
import bs4
from website_mapping import scrape_articles
from selenium_call import get_article_list

sources = pd.read_csv("sources.csv")

for index, source in sources.iterrows():
    link = sources['link'][index]
    journal = sources['title'][index]

    page = get_article_list(url = link, source = journal)
    soup = bs4.BeautifulSoup(page)
    df = scrape_articles(soup, journal)
    print(df)

link = sources['link'][5]
journal = sources['title'][5]

page = get_article_list(url = link, source = journal)
soup = bs4.BeautifulSoup(page)

df = scrape_articles(soup, journal)
