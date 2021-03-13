#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Alessio Nardin
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

sources = pd.read_csv("sources.csv")
print(sources)

for index, website in sources.iterrows():
    print(website['link'])

link = sources['link'][0]

driver = webdriver.Firefox()

driver.get(link)

html_source = driver.page_source

print(html_source)

html_source
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
#driver.close()
