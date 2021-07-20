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

def eea(url, driver, date):

    driver.get(url)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="entries"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'tileItem visualIEFloatFix'})
        for item in list_item:
            title = item.a.img['title']
            link = item.a['href']
            pub_date = item.div.span.text
            snippet = item.p.span.text
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
            button = driver.find_element_by_xpath('//a[@class="next"]')
            button.click()

        time.sleep(2)

    return final_df

def eib(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="search-filter__results row card-row-items"]')


        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("h3", {"class": "card-row-title margin-right-20"})
        for item in list_item:
            title = item.a.text.strip()
            link = 'https://www.eib.org' + item.a['href']
            titles.append(title)
            links.append(link)
        list_item = soup.find_all("span", {"class": "card-row-date"})
        for item in list_item:
            pub_date = item.text.strip()
            pub_dates.append(pub_date)

        list_item = soup.find_all("div", {"class": "card-row-text"})
        for item in list_item:
            snippet = item.text.strip()
            snippets.append(snippet)


        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date, settings={'DATE_ORDER': 'DMY'}).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@class="nextPrevPagination nextPagination"]')
            button.click()

        time.sleep(2)

    return final_df

# EIF HAS A DIFFERENT PAGE, CHECK LINK
def eif(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="search-filter__results row card-row-items"]')


        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("h3", {"class": "card-row-title margin-right-20"})
        for item in list_item:
            title = item.a.text.strip()
            link = 'https://www.eib.org' + item.a['href']
            titles.append(title)
            links.append(link)
        list_item = soup.find_all("span", {"class": "card-row-date"})
        for item in list_item:
            pub_date = item.text.strip()
            pub_dates.append(pub_date)

        list_item = soup.find_all("div", {"class": "card-row-text"})
        for item in list_item:
            snippet = item.text.strip()
            snippets.append(snippet)


        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date, settings={'DATE_ORDER': 'DMY'}).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@class="nextPrevPagination nextPagination"]')
            button.click()

        time.sleep(2)

    return final_df

def eit(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        try:
            cookies = driver.find_element_by_xpath('//button[@class="agree-button"]')
            cookies.click()
        except:
            print("cookies are already ok")

        article_containers = driver.find_element_by_xpath('//div[@class="news eit-list"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.findAll("li")
        for item in list_item:
            title = item.a.text
            link = 'https://eit.europa.eu' + item.a['href']
            pub_date = item.span.text
            snippet = ''
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
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def enicbcmed(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        try:
            cookies = driver.find_element_by_xpath('//button[@class="decline-button eu-cookie-compliance-default-button"]')
            cookies.click()
        except:
            print("cookies are already ok")

        article_containers = driver.find_element_by_xpath('//div[@class="block-items"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'block-body-content'})
        for item in list_item:
            title = item.a.h6.text.strip()
            link = 'http://www.enicbcmed.eu/' + item.a['href']
            snippet = item.p.text.strip()
            titles.append(title)
            links.append(link)
            snippets.append(snippet)
        list_item = soup.find_all('time', {'class':'datetime'})
        for item in list_item:
            pub_date = item['datetime']
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

## there are two more sections to check
def espon(url, driver, date):

    driver.get(url)
    time.sleep(3)
    counter = 1
    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_elements_by_xpath('//ul[@class="recent-posts"]')[3]

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'views-field views-field-title'})
        for item in list_item:
            title = item.span.a.text
            link = 'https://www.espon.eu' + item.span.a['href']
            titles.append(title)
            links.append(link)
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

        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            counter = counter + 1
            pagenum = "Go to page " + str(counter) + '\"]'
            button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            button.click()

        time.sleep(2)

    return final_df

def eucommission(url, driver, date):

    driver.get(url)
    time.sleep(3)
    counter = 1

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_elements_by_xpath('//section[@id="news-block"]')[0]

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.section.ul.find_all("div", {"_ngcontent-c1": ""})
        for item in list_item:
            article = item.li
            if type(article) is bs4.element.Tag:
                category = item.div.div.span.text
                pub_date = item.div.div.find_all("span", {"ngcontent-c1":""})[1].text
                link = 'https://ec.europa.eu/commission/presscorner/' + article.a['href']
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

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            counter = counter + 1
            pagenum = "Go to page " + str(counter) + '\"]'
            button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            button.click()

        time.sleep(2)

    return final_df

def euparliament(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        try:
            cookies = driver.find_element_by_xpath('//span[contains(text(), "Rifiuto i cookie analitici")]')
            cookies.click()
        except:
            print("cookies are already ok")

        article_containers = driver.find_element_by_xpath('//div[@class="ep_gridrow ep-o_productlist"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("div", {"class":"ep_title"})
        for item in list_item:
            title = item.a.div.span.text.strip()
            link = item.a['href']
            titles.append(title)
            links.append(link)
        list_item = soup.find_all("div", {"class":"ep-a_text"})
        for item in list_item:
            snippet = item.text.strip()
            snippets.append(snippet)

        list_item = soup.find_all("time", {"itemprop": "datePublished"})
        for item in list_item:
            pub_date = item['datetime']
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            final_df = pd.DataFrame()
            button = driver.find_element_by_xpath('//a[@id="continuesLoading_button"]')
            button.click()


        time.sleep(2)

    return final_df

def euregha(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="et_pb_blog_grid clearfix  et_pb_text_align_center"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('article')
        for item in list_item:
            title = item.h4.text
            link = item.h4.a['href']
            pub_date = item.p.text
            snippet = ''
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
            button = driver.find_element_by_xpath("//a[contains(text(), 'Older Entries')]")
            button.click()


        time.sleep(2)

    return final_df

def europeanagency(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        try:
            cookies = driver.find_element_by_xpath('//button[@class="decline-button eu-cookie-compliance-default-button"]')
            cookies.click()
        except:
            print("cookies are already ok")

        article_containers = driver.find_element_by_xpath('//div[@class="view-content"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('h3', {'class':'views-field views-field-title'})
        for item in list_item:
            title = item.a.text.strip()
            link = 'https://www.europeanagency.org' + item.a['href']
            snippet = item.next_sibling
            titles.append(title)
            links.append(link)
            if snippet != '':
                snippets.append(snippet)

        list_item = soup.find_all('footer', {'class':'views-field views-field-created'})
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
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def eurostat(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//ul[@class="product-list"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("div", {"class": "product-title"})
        for item in list_item:
            title = item.text.strip()
            link = item.a['href']
            snippet = ''

            titles.append(title)
            links.append(link)
            snippets.append(snippet)

        list_item = soup.find_all("div", {"class": "product-date"})
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
            button = driver.find_element_by_xpath('//a[contains(text(), "Next")]')
            button.click()

        time.sleep(2)

    return final_df

def eusalp(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    try:
        cookies = driver.find_element_by_xpath('//button[@class="decline-button eu-cookie-compliance-default-button"]')
        cookies.click()
    except:
        print("cookies are already ok")


    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="view-content"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all("h3", {"class": "views-field views-field-title event-box-title"})
        for item in list_item:
            title = item.span.a.text
            link = 'https://www.alpine-region.eu' + item.span.a['href']
            links.append(link)
            titles.append(title)

        list_item = soup.find_all("span", {"class": "date-display-single"})
        for item in list_item:
            pub_date = item.text
            pub_dates.append(pub_date)

        list_item = soup.find_all("div", {"class": "views-field views-field-body"})
        for item in list_item:
            snippet = item.span.text
            snippets.append(snippet)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

## ONLY GETS 2021, even if 2020 and 2019 are on the same page
def imi(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()


    titles = []
    links = []
    pub_dates = []
    snippets = []

    article_containers = driver.find_element_by_xpath('//div[@class="view-grouping-content info-box light-grey-bg"]')

    article_containers = article_containers.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(article_containers, 'lxml')

    list_item = soup.find_all("div", {"class": "views-row article-row"})

    for item in list_item:
        title = item.div.span.article.div.div.h4.text
        link = 'https://www.imi.europa.eu' + item.div.span.article.div.div.h4.a['href']
        titles.append(title)
        links.append(link)

    list_item = soup.find_all("span", {"class": "published-date"})
    for item in list_item:
        pub_date = item.text
        pub_dates.append(pub_date)

    list_item = soup.find_all("div", {"class": "field field--name-body field--type-text-with-summary field--label-hidden field--item"})
    for item in list_item:
        snippet = item.text
        snippets.append(snippet)

    for index, one_date in enumerate(pub_dates):
        pub_dates[index] = dateparser.parse(one_date).date()
    df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)), columns =['title', 'pub_date', 'snippet', 'link'])

    final_df = final_df.append(df)

    time.sleep(2)

    return final_df

## INTERACT is still missing

def interreg(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="content-area"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('section', {'class','search-result__item search-result__item--news'})
        for item in list_item:
            title = item.find('div', {'class':'search-result__item__title'})
            link = title.a['href']
            title = title.a.text.strip()
            pub_date = item.find('span', {'class': 'bold'}).text
            snippet = item.find('div', {'class':'clamp-this__2-lines'}).text.strip()
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
            button = driver.find_element_by_xpath('//a[@aria-label="Next"]')
            button.click()

        time.sleep(2)

    return final_df

def jrc(url, driver, date):
    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="block block-system panel panel-default clearfix"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'ds-1col node node-news view-mode-apache_solr_mode clearfix'})
        for item in list_item:
            titletag = item.find('div', {'class':'field field-name-title field-type-ds field-label-hidden'})
            title = titletag.h3.text
            link = 'https://ec.europa.eu' + titletag.a['href']
            snippet = item.find('div', {'property':'content:encoded'}).text.strip()
            pub_date = item.find('div', {'class':'date-cont start-date'}).text.strip()
            titles.append(title)
            links.append(link)
            snippets.append(snippet)
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)

        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def promis(url, driver, date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles = []
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@id="boxNotizieArchivio"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('div', {'class':'notiziaConFoto'})
        for item in list_item:
            title = item.find('h1').text.strip()
            link = 'https://www.promisalute.it' + item.find('a')['href']
            snippet = item.find('h3').text.strip()
            pub_date = item.find('h2').text.strip()
            pub_date = pub_date.split('\n')[1].strip()
            titles.append(title)
            links.append(link)
            snippets.append(snippet)
            pub_dates.append(pub_date)

        for index, one_date in enumerate(pub_dates):
            pub_dates[index] = dateparser.parse(one_date).date()
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)


        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@id="formid_ElencoNotizie_Paginazione_Paginazione_Link_Successiva"]')
            button.click()

        time.sleep(2)

    return final_df

def urbact(url, driver, date):
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
        links = []
        pub_dates = []
        snippets = []

        article_containers = driver.find_element_by_xpath('//div[@class="panel-pane pane-views-panes pane-urbact-articles-article-list-news"]')

        article_containers = article_containers.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(article_containers, 'lxml')

        list_item = soup.find_all('h2', {'class':'node__title node-title'})
        for item in list_item:
            title = item.a.text
            link = 'https://urbact.eu' + item.a['href']
            titles.append(title)
            links.append(link)
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
        df = pd.DataFrame(list(zip(titles, pub_dates, snippets, links)),
                        columns =['title', 'pub_date', 'snippet', 'link'])

        final_df = final_df.append(df)

        counter = counter + 1
        if df.iloc[len(df) - 1]['pub_date'] <= date:
            is_paginated = False
        elif counter < 6:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df
