import pandas as pd
from navigate import get_article_list
from parse import scrape_articles

sources = pd.read_csv('sources.csv')
#sources = pd.DataFrame(sources.iloc[58]).transpose()
#url = sources['link'].iloc[0]
final_df = pd.DataFrame()
for i, source in sources.iterrows():

    try:
        if source['status'] == 'active':

            print(source['website'])

            # Getting html page
            html_page = get_article_list(source['link'], source['website'])

            # Parse html
            df = scrape_articles(html_page, source['website'])

            if i != 0:
                df.to_csv('newsletter.csv', mode = 'a', header = False, index = False)
            else:
                df.to_csv('newsletter.csv', mode = 'a', header = True, index = False)
    except:
        print('There has been an error')
