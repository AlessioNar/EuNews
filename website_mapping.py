import bs4
import pandas as pd
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
    else:
        print("There is not yet a retrieval method for this website")
        return 1

    df = pd.DataFrame(list(zip(titles, links, pub_dates, snippets)),
                    columns =['title', 'link', 'pub_date', 'snippet'])

    df['source'] = source

    return df
