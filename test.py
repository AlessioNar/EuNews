from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from websites import *

driver = webdriver.Firefox()
date = datetime.date(2021,5,10)

sources = pd.read_csv('sources_short.csv')
df = pd.DataFrame(columns =['title', 'pub_date', 'snippet', 'url'])

for i, entry in sources.iterrows():
    driver.get(entry['link'])
    if entry['website'] == 'apre':
        source = Apre(entry['website'], entry['link'], entry['status'])
    elif entry['website'] == 'areflh':
        source = Areflh(entry['website'], entry['link'], entry['status'])

    # Get container
    container = source.get_container(driver)
    # Get soup
    soup = source.get_soup(container)
    # Get articles

    temp_df = source.get_articles(soup)
    df = pd.concat([df, temp_df]).reset_index(drop=True)



for article in df:
    print(article.title)
    print(article.pub_date)
    print(article.snippet)
    print(article.url)

df.title
df.pub_date
df.snippet
df.url

pd.DataFrame(data = df)
list = range(10)

container = container.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(container, 'lxml')
source.get_articles()

## I should have included all websites

url = 'http://www.areflh.org/index.php?lang=en'


driver.get(url)

urbact(url, driver, date)

final_df = pd.DataFrame()
