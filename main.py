import pandas as pd
from navigate import get_article_list
from parse import scrape_articles

sources = pd.read_csv('sources.csv')
sources = pd.DataFrame(sources.iloc[3]).transpose()
url = sources['link'].iloc[0]

for i, source in sources.iterrows():

    try:
        if source['status'] == 'active':

            print(source['website'])

            # Getting html page
            html_page = get_article_list(source['link'], source['website'])
            #html_page = get_article_list(url, sources['website'].iloc[0])

            # Parse html
            df = scrape_articles(html_page, source['website'])
            #df = scrape_articles(html_page, sources['website'].iloc[0])
            df_length = len(df.index)

            if df['pub_date'].iloc[df_length - 1] <= start:
                #stop
            else:
                #go on with pagination

            if i != 0:
                df.to_csv('newsletter.csv', mode = 'a', header = False, index = False)
            else:
                df.to_csv('newsletter.csv', mode = 'a', header = True, index = False)
    except:
        print('There has been an error')
