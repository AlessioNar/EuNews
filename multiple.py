from website_mapping import scrape_articles
from selenium_call import get_article_list
from db_operations import add_articles
from db_operations import most_recent_date

def scrape(journal, link):
    print("Scraping " + journal)
    ## Here I could create a while loop that integrates a condition when we reach the date of the last last_update
    ## It stops paginating
    try:
        soup = get_article_list(url = link, source = journal)
    except:
        print("Error during webscraping " + journal)
    print("Parsing " + journal)

    last_updated = most_recent_date(journal)
    print(journal + " most recent article was published in " + str(last_updated))

    try:
        temp_df = scrape_articles(soup, journal)
    except:
        print("Error during parsing " + journal)


    print("Inserting new articles in database")
    print("There are " + " new articles " + " from " + journal)

    add_articles(temp_df)
