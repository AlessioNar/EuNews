import bs4
from datetime import datetime
import dateparser
import numpy as np
import pandas as pd

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
