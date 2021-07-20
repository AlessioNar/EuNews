import bs4
from datetime import date, datetime, timedelta
import dateparser
import numpy as np
import pandas as pd
import re

# Apre is ok, no need to filter articles
def apre(url, driver):
    titles = []
    links = []
    pub_dates = []
    snippets = []
    driver.get(url)
    article_containers = driver.find_elements_by_xpath('//main[@class="site-main"]')[0]
    article_containers = article_containers.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(article_containers, 'lxml')
    list_item = soup.find_all('h2', {'class':'entry-title'})
    for item in list_item:
        title = item.text.strip()
        link = item.a['href']
        titles.append(title)
        links.append(link)
    list_item = soup.find_all('span', {'class':'published'})
    for item in list_item:
        pub_date = item.text.strip()
        pub_dates.append(pub_date)
    list_item = soup.find_all('div', {'id':'bottom-blog'})
    for item in list_item:
        snippet = item.text.strip()
        snippets.append(snippet)
    for index, one_date in enumerate(pub_dates):
        pub_dates[index] = dateparser.parse(one_date)
        pub_dates[index] = np.datetime64(pub_dates[index]).astype(datetime)
    df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                    columns =['title', 'pub_date', 'snippet', 'link'])
    return df

def areflh(url, driver):
    titles = []
    links = []
    pub_dates = []
    snippets = []
    driver.get(url)
    article_containers = driver.find_elements_by_xpath('//div[@class="uk-container"]')[1]
    article_containers = article_containers.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(article_containers, 'lxml')

    list_item = soup.find_all("h3", {"class": "el-title uk-card-title uk-margin-top uk-margin-remove-bottom"})
    for item in list_item:
        title = item.text.strip()
        titles.append(title)

    list_item = soup.find_all("a", {"class": "el-item uk-card uk-card-default uk-card-hover uk-link-toggle uk-display-block"})
    for item in list_item:
        link = 'https://www.areflh.org' + item['href']
        links.append(link)

    list_item = soup.find_all("div", {"class": "el-meta uk-text-meta uk-margin-top"})
    for item in list_item:
        pub_date = re.sub('Publié le', '', item.text).strip()
        pub_dates.append(pub_date)

    list_item = soup.find_all("div", {"class": "el-content uk-panel uk-margin-top"})
    for item in list_item:
        if item.p:
            snippet = item.p.text
        else:
            snippet = item.div.text
        snippets.append(snippet)

    for index, one_date in enumerate(pub_dates):
        pub_dates[index] = dateparser.parse(one_date)
        pub_dates[index] = np.datetime64(pub_dates[index]).astype(datetime)
    df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                    columns =['title', 'pub_date', 'snippet', 'link'])
    return df

# This is ok and it works. I just need to provide the end date and then
# Eventually filter the results
def consigliodeuropait(url, driver, date):

    driver.get(url)

    is_paginated = True
    final_df = pd.DataFrame()
    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []
        article_containers = driver.find_elements_by_xpath('//div[@class="newsroom "]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("div", {"class": "element clearfix"})
        for item in list_item:
            title = item.h3.text.strip()
            link = item.h3.a['href']
            upper = item.find_all("div", {"class": "upper"})[0]
            pub_date = upper.find_all("span", {"class":"date"})[0].text
            snippet = item.p.text.strip()

            titles.append(title)
            links.append(link)
            pub_dates.append(pub_date)
            snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath("//a[contains(text(), 'seguente')]")
            button.click()

    return final_df
