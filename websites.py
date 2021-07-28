import bs4
from datetime import date, datetime
import dateparser
import pandas as pd
import re
import time

## there are two more sections to check
def espon(url, driver, max_date):

    driver.get(url)
    time.sleep(3)
    counter = 1
    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        urls = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_elements_by_xpath('//ul[@class="recent-posts"]')[3]

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'views-field views-field-title'})
        for item in list_item:
            title = item.span.a.text
            url = 'https://www.espon.eu' + item.span.a['href']
            titles.append(title)
            urls.append(url)
        list_item = soup.find_all('div', {'class':'views-field views-field-created'})
        for item in list_item:
            pub_date = item.span.small.span.next_sibling
            pub_dates.append(pub_date)
        list_item = soup.find_all('li')
        for item in list_item:
            snippet = item.find_next('div').find_next('div').find_next('div').find_next('div').find_next('div').find_next('div').find_next('div').p.text.strip()
            snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)),
                        columns =['title', 'pub_date', 'snippet', 'url'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            counter = counter + 1
            pagenum = "Go to page " + str(counter) + '\"]'
            button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            button.click()

        time.sleep(2)

    return final_df

## INTERACT is still missing
def interreg(url, driver, max_date):

    driver.get(url)
    time.sleep(3)
    try:
        cookies = driver.find_element_by_xpath("//a[@class='cc-btn cc-deny']")
        cookies.click()
    except:
        print('cookies are already ok')
    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        urls = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="content-area"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('section', {'class','search-result__item search-result__item--news'})
        for item in list_item:
            title = item.find('div', {'class':'search-result__item__title'})
            url = title.a['href']
            title = title.a.text.strip()
            pub_date = item.find('span', {'class': 'bold'}).text
            snippet = item.find('div', {'class':'clamp-this__2-lines'}).text.strip()
            titles.append(title)
            urls.append(url)
            pub_dates.append(pub_date)
            snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)),
                        columns =['title', 'pub_date', 'snippet', 'url'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@aria-label="Next"]')
            button.click()

        time.sleep(2)

    return final_df

def jrc(url, driver, max_date):
    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        urls = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="block block-system panel panel-default clearfix"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'ds-1col node node-news view-mode-apache_solr_mode clearfix'})
        for item in list_item:
            titletag = item.find('div', {'class':'field field-name-title field-type-ds field-label-hidden'})
            title = titletag.h3.text
            url = 'https://ec.europa.eu' + titletag.a['href']
            snippet = item.find('div', {'property':'content:encoded'}).text.strip()
            pub_date = item.find('div', {'class':'date-cont start-date'}).text.strip()
            titles.append(title)
            urls.append(url)
            snippets.append(snippet)
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)),
                        columns =['title', 'pub_date', 'snippet', 'url'])

        final_df = final_df.append(df)

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def promis(url, driver, max_date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        urls = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@id="boxNotizieArchivio"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'notiziaConFoto'})
        for item in list_item:
            title = item.find('h1').text.strip()
            url = 'https://www.promisalute.it' + item.find('a')['href']
            snippet = item.find('h3').text.strip()
            pub_date = item.find('h2').text.strip()
            pub_date = pub_date.split('\n')[1].strip()
            titles.append(title)
            urls.append(url)
            snippets.append(snippet)
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)),
                        columns =['title', 'pub_date', 'snippet', 'url'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@id="formid_ElencoNotizie_Paginazione_Paginazione_Link_Successiva"]')
            button.click()

        time.sleep(2)

    return final_df

def ecgeneric(url, driver, max_date):

    driver.get(url)
    time.sleep(3)
    counter = 1

    is_paginated = True
    df = pd.DataFrame()
    try:
        closepopup = driver.find_element_by_xpath("//a[@id='ec-survey-pop-up-body-button-do-not-participate']")
        closepopup.click()
    except:
        print('no survey')

    try:
        cookies = driver.find_element_by_xpath("//a[@class='cck-actions-button']")
        cookies.click()
        closecookies = driver.find_element_by_xpath("//a[@href='#close']")
        closecookies.click()
    except:
        print('no cookies')

    while is_paginated:
        titles, urls, pub_dates, snippets = initialize_lists()

        container = driver.find_element_by_xpath('//div[@class="view-content"]')

        soup = get_soup(container)

        list_item = soup.find_all("div", {"class": "listing__column-main"})
        for item in list_item:
            title = item.div.next_sibling.text.strip()
            url = item.div.next_sibling.a['href']
            pub_date = item.div.span.next_sibling.text.strip()
            snippet = '' #item.find_all('p')
            #if snippet == '':
            #    snippet = ''
            #else:
            #    snippet = snippet.text.strip()

            titles.append(title)
            pub_dates.append(pub_date)
            urls.append(url)
            snippets.append(snippet)
        temp_df = create_df(titles, pub_dates, snippets, urls)
        df = df.append(temp_df)

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath("//a[@title='Vai alla pagina successiva']")
            button.click()

        time.sleep(5)

    return df

def ecitalia(url, driver, max_date):

    driver.get(url)
    time.sleep(3)
    counter = 1

    is_paginated = True
    df = pd.DataFrame()
    try:
        closepopup = driver.find_element_by_xpath("//a[@id='ec-survey-pop-up-body-button-do-not-participate']")
        closepopup.click()
    except:
        print('no survey')

    try:
        cookies = driver.find_element_by_xpath("//a[@class='cck-actions-button']")
        cookies.click()
        closecookies = driver.find_element_by_xpath("//a[@href='#close']")
        closecookies.click()
    except:
        print('no cookies')

    while is_paginated:
        titles, urls, pub_dates, snippets = initialize_lists()

        container = driver.find_element_by_xpath('//div[@class="ecl-content-item-block"]')

        soup = get_soup(container)

        list_item = soup.find_all("article")
        for item in list_item:
            title = item.div.next_sibling.div.next_sibling.a.text.strip()
            url = 'https://italy.representation.ec.europa.eu' + item.div.next_sibling.div.next_sibling.a['href']
            pub_date = item.div.next_sibling.div.time['datetime']
            snippet = '' #item.find_all('p')
            #if snippet == '':
            #    snippet = ''
            #else:
            #    snippet = snippet.text.strip()

            titles.append(title)
            pub_dates.append(pub_date)
            urls.append(url)
            snippets.append(snippet)
        temp_df = create_df(titles, pub_dates, snippets, urls)
        df = df.append(temp_df)

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath("//a[@class='ecl-link ecl-link--standalone ecl-link--icon ecl-link--icon-after ecl-pagination__link']")
            button.click()

        time.sleep(5)

    return df

def urbact(url, driver, max_date):
    counter = 1
    driver.get(url)
    time.sleep(3)

    try:
        cookies = driver.find_element_by_xpath('//button[@class="decline-button eu-cookie-compliance-default-button"]')
        cookies.click()
    except:
        print("cookies are already ok")

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        urls = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="panel-pane pane-views-panes pane-urbact-articles-article-list-news"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('h2', {'class':'node__title node-title'})
        for item in list_item:
            title = item.a.text
            url = 'https://urbact.eu' + item.a['href']
            titles.append(title)
            urls.append(url)
        list_item = soup.find_all('time', {'pubdate':''})
        for item in list_item:
            pub_date = item['datetime']
            pub_dates.append(pub_date)
        list_item = soup.find_all('div', {'class':'field-item even'})
        for item in list_item:
            snippet = item.text.strip()
            if snippet != '':
                snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, urls)),
                        columns =['title', 'pub_date', 'snippet', 'url'])

        final_df = final_df.append(df)

        counter = counter + 1
        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        elif counter < 6:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df
