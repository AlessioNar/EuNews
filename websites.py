import bs4
from datetime import date, datetime
import dateparser
import pandas as pd
import re
import time

def eit(url, driver, max_date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles, links, pub_dates, snippets = initialize_lists()

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

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def enicbcmed(url, driver, max_date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    df = pd.DataFrame()
    counter = 0
    while is_paginated:
        titles, links, pub_dates, snippets = initialize_lists()

        try:
            cookies = driver.find_element_by_xpath('//button[@class="decline-button eu-cookie-compliance-default-button"]')
            cookies.click()
        except:
            print("cookies are already ok")

        container = driver.find_element_by_xpath('//div[@class="block-items"]')

        soup = get_soup(container)

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

        temp_df = create_df(titles, pub_dates, snippets, links)
        df = df.append(temp_df)

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            counter = counter + 1
            next_page = 'http://www.enicbcmed.eu/info-center/news?field_tags_target_id=All&keys=&page=' + str(counter)
            driver.get(next_page)

        time.sleep(2)

    return df

## there are two more sections to check
def espon(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            counter = counter + 1
            pagenum = "Go to page " + str(counter) + '\"]'
            button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            button.click()

        time.sleep(2)

    return final_df

def eucommission(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            counter = counter + 1
            pagenum = "Go to page " + str(counter) + '\"]'
            button = driver.find_element_by_xpath('//a[@title=\"' + pagenum)
            button.click()

        time.sleep(2)

    return final_df

def euparliament(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            final_df = pd.DataFrame()
            button = driver.find_element_by_xpath('//a[@id="continuesLoading_button"]')
            button.click()


        time.sleep(2)

    return final_df

def euregha(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath("//a[contains(text(), 'Older Entries')]")
            button.click()


        time.sleep(2)

    return final_df

def europeanagency(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

def eurostat(url, driver, max_date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    final_df = pd.DataFrame()

    while is_paginated:
        titles, links, pub_dates, snippets = initialize_lists()

        container = driver.find_element_by_xpath('//ul[@class="product-list"]')

        soup = get_soup(container)

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

        temp_df = create_df(titles, pub_dates, snippets, links, dayfirst=True)

        df = df.append(temp_df)

        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[contains(text(), "Next")]')
            button.click()

        time.sleep(2)

    return df

def eusalp(url, driver, max_date):

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


        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        else:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df

## ONLY GETS 2021, even if 2020 and 2019 are on the same page
def imi(url, driver, max_date):

    driver.get(url)
    time.sleep(3)

    is_paginated = True
    df = pd.DataFrame()

    titles, links, pub_dates, snippets = initialize_lists()
    container = driver.find_element_by_xpath('//div[@class="view-grouping-content info-box light-grey-bg"]')

    soup = get_soup(container)

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

    temp_df = create_df(titles, pub_dates, snippets, links, dayfirst=True)

    df = df.append(temp_df)

    time.sleep(2)

    return df

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
        titles, links, pub_dates, snippets = initialize_lists()

        container = driver.find_element_by_xpath('//div[@class="view-content"]')

        soup = get_soup(container)

        list_item = soup.find_all("div", {"class": "listing__column-main"})
        for item in list_item:
            title = item.div.next_sibling.text.strip()
            link = item.div.next_sibling.a['href']
            pub_date = item.div.span.next_sibling.text.strip()
            snippet = '' #item.find_all('p')
            #if snippet == '':
            #    snippet = ''
            #else:
            #    snippet = snippet.text.strip()

            titles.append(title)
            pub_dates.append(pub_date)
            links.append(link)
            snippets.append(snippet)
        temp_df = create_df(titles, pub_dates, snippets, links)
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
        titles, links, pub_dates, snippets = initialize_lists()

        container = driver.find_element_by_xpath('//div[@class="ecl-content-item-block"]')

        soup = get_soup(container)

        list_item = soup.find_all("article")
        for item in list_item:
            title = item.div.next_sibling.div.next_sibling.a.text.strip()
            link = 'https://italy.representation.ec.europa.eu' + item.div.next_sibling.div.next_sibling.a['href']
            pub_date = item.div.next_sibling.div.time['datetime']
            snippet = '' #item.find_all('p')
            #if snippet == '':
            #    snippet = ''
            #else:
            #    snippet = snippet.text.strip()

            titles.append(title)
            pub_dates.append(pub_date)
            links.append(link)
            snippets.append(snippet)
        temp_df = create_df(titles, pub_dates, snippets, links)
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
        if df.iloc[len(df) - 1]['pub_date'] <= max_date:
            is_paginated = False
        elif counter < 6:
            button = driver.find_element_by_xpath('//a[@title="Go to next page"]')
            button.click()

        time.sleep(2)

    return final_df
