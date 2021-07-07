import pandas as pd
from multiple import scrape
from db_operations import create_table

def main():

    create_table()
    # Open sources
    sources = pd.read_csv("sources.csv")

    df = pd.DataFrame()

    # Open database
    for index, source in sources.iterrows():
        link = sources['link'][index]
        journal = sources['title'][index]
        temp_df = scrape(journal, link)


if __name__ == '__main__':
    main()

#link = sources['link'][2]
#journal = sources['title'][2]

#page = get_article_list(url = link, source = journal)
#soup = bs4.BeautifulSoup(page)

#df = scrape_articles(soup, journal)
