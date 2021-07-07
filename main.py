import pandas as pd
from selenium_call import get_article_list
from website_mapping import scrape_articles

sources = pd.read_csv('sources.csv')
sources = pd.DataFrame(sources.iloc[18]).transpose()

for i, source in sources.iterrows():

    if source['status'] == 'active':

        print(source['website'])

        # Getting html page
        html_page = get_article_list(source['link'], source['website'])

        # Parse html
        df = scrape_articles(html_page, source['website'])
        print(df)

url = sources['link'].iloc[0]
