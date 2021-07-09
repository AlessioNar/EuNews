import pandas as pd
from navigate import get_article_list
from parse import scrape_articles

sources = pd.read_csv('sources.csv')
sources = pd.DataFrame(sources.iloc[50]).transpose()
url = sources['link'].iloc[0]

for i, source in sources.iterrows():

    if source['status'] == 'active':

        print(source['website'])

        # Getting html page
        html_page = get_article_list(source['link'], source['website'])

        # Parse html
        df = scrape_articles(html_page, source['website'])
        print(df)
