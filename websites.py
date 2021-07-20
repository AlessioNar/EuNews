import bs4
from datetime import date, datetime, timedelta
import dateparser
import numpy as np
import pandas as pd
import re
import time
from selenium.webdriver.common.action_chains import ActionChains

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

# Working
def consiglioeuropeo(url, driver, date):
    counter = 1
    driver.get(url)

    try:
        cookies = driver.find_elements_by_xpath('//span[@id="reject_cookies"]')[0]
        cookies.click()
    except:
        print('Cookies are already rejected')
    is_paginated = True
    final_df = pd.DataFrame()
    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []
        article_containers = driver.find_elements_by_xpath('//div[@class="col-md-9 council-flexify-item pull-right"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("ul", {"class": "list-group"})
        for item in list_item:
            pub_date = item.li.h2.time['datetime']
            article_containers = item.li.ul
            for article in article_containers:
                if type(article) is bs4.element.Tag:
                    title = article.div.h3.text
                    link = 'https://www.consilium.europa.eu' + article.div.h3.a['href']
                    snippet = article.p.text
                    links.append(link)
                    titles.append(title)
                    snippets.append(snippet)
                    pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)

        counter = counter+1

        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            driver.get(url+'?Page='+str(counter))
            time.sleep(3)

            #driver.execute_script("window.scrollTo(0, 3500);")
            #button = driver.find_element_by_xpath('//li[@aria-label="Vai alla pagina successiva"]')
            #button.click()

    return final_df

# COR websites contains only 5 pages!
def cor(url, driver, date):

    driver.get(url)

    is_paginated = True
    final_df = pd.DataFrame()
    counter = 1
    while is_paginated:

        titles = []
        links = []
        pub_dates = []
        snippets = []
        article_containers = driver.find_elements_by_xpath('//div[@class="cbq-layout-main"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("div", {"class":"col-md-6 card"})
        for item in list_item:
            try:
                if item['hidden'] == '':
                    dummy = 'hidden'
            except:
                title = item.text.strip()
                link = item.a['href']
                pub_date = item.find("div", {"class":"HighlightDateLine"})
                try:
                    pub_date = pub_date.text.split('Press release')[1]
                except:
                    pub_date = pub_date.text
                pub_date = pub_date.split('|')[0].strip()
                snippet = item.a.div.div.div.next_sibling.text.strip()
                titles.append(title)
                links.append(link)
                pub_dates.append(pub_date)
                snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date, settings={'DATE_ORDER': 'DMY'}).date()

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            if counter == 1:
                # trova navbar e clicca per andare sul 3
                navbar = driver.find_element_by_xpath('//div[@class="cor-pagination-container bottom-pagination"]')
                navbar.click()

                # torna sul 2
                navbar = driver.find_element_by_xpath('//i[@class="fa fa-arrow-left"]')
                navbar.click()
                counter = counter + 1
            elif counter == 5:
                break
            else:
                navbar = driver.find_element_by_xpath('//li[@class="page-item next"]')
                navbar.click()
                counter = counter + 1


        time.sleep(2)

    return final_df

def cprm(url, driver, date):

    driver.get(url)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@id="posts-container"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'fusion-post-content post-content'})
        for item in list_item:
            title = item.h2.text.strip()
            link = item.h2.a['href']
            snippet = item.div.p.text.strip()
            titles.append(title)
            links.append(link)
            snippets.append(snippet)
        list_item = soup.find_all('div', {'class':'fusion-date-box'})
        for item in list_item:
            pub_date = item.text.strip()
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)

    return final_df

def earlall(url, driver, date):

    driver.get(url)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@id="content-full"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('li')
        for item in list_item:
            title = item.h3.text.strip()
            link = item.a['href']
            snippet = item.p.find_next().find_next().text
            pub_date = item.p.find_next().find_next().find_next().text
            titles.append(title)
            links.append(link)
            snippets.append(snippet)
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date, settings={'DATE_ORDER': 'DMY'}).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@class="nextpostslink"]')
            button.click()

        time.sleep(2)

    return final_df
