import bs4
import pandas as pd
from datetime import datetime
import dateparser
import numpy as np

def scrape_articles(soup, source):

    titles = []
    links = []
    pub_dates = []
    snippets = []

    if source == 'eucommission':
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

    elif source == 'consiglioeuropeo':
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

    elif source == 'consigliodeuropait':
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
            pub_date = pub_date.text
            location = upper.findAll("span", {"class":"location"})[0]
            snippet = article.p.text.strip()
            titles.append(title)
            links.append(link)
            pub_dates.append(pub_date)
            snippets.append(snippet)

    elif source == 'esma':
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

    elif source == 'horizon2020':
        articles = soup.findAll("li", class_="listing__item")
        for article in articles:
            title = article.div.div.h2.a.text
            link = article.div.div.h2.a['href']
            container = article.div.div.div
            second_container = container.findAll("div", class_="required-fields meta group-meta field-group-meta_wrapper")[0]
            pub_date = second_container.div.div.div.span['content']
            second_container = container.findAll("div", class_="field field-name-field-newsroom-teaser field-type-text-long field-label-hidden")[0]
            snippet = second_container.div.div.text
            titles.append(title)
            links.append(link)
            pub_dates.append(pub_date)
            snippets.append(snippet)

    elif source == 'easme':
        articles = soup.findAll("li")
        for article in articles:
            container = article.findAll("div", class_="row")[0]
            container = container.findAll("div", class_="col-xs-12 col-sm-9")[0]
            title = container.a.h3.text
            link = container.a['href']
            snippet_container = container.findAll("div", class_="ecl-list-item__detail ecl-paragraph")[0]
            snippet = snippet_container.text
            date_container = container.findAll("div", class_="ecl-meta ecl-meta--three-columns")[0]
            # This needs to be fixed, now it returns None
            pub_date = date_container.span.text
            titles.append(title)
            links.append(link)
            pub_dates.append(pub_date)
            snippets.append(snippet)

    elif source == 'eit':
        articles = soup.findAll("li")
        for article in articles:
            title = article.a.text
            link = article.a['href']
            pub_date = article.span.text
            snippet = ''
            titles.append(title)
            links.append(link)
            pub_dates.append(pub_date)
            snippets.append(snippet)
    else:
        print("There is not yet a retrieval method for this website")
        return 1

    for index, one_date in enumerate(pub_dates):
        pub_dates[index] = dateparser.parse(one_date)
        pub_dates[index] = np.datetime64(pub_dates[index]).astype(datetime)

    df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
                    columns =['title', 'link', 'pub_date', 'snippet'])

    df['source'] = source

    return df
