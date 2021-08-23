from selenium import webdriver
from datetime import date
import pandas as pd
from parsers import *

from db_operations import *

create_table()

target_date = date(2021, 8, 17)

sources = pd.read_csv('sources.csv')
sources = sources.loc[sources['status'] == 'active']

driver = webdriver.Firefox()

for index, website in sources.iterrows():
    print(website['website'])
    if website['website'] == 'apre':
        scraper = ApreScraper(driver, target_date)
    elif website['website'] == 'apre_eventi':
        scraper = ApreEventScraper(driver, target_date)
    elif website['website'] == 'areflh':
        scraper = AreflhScraper(driver, target_date)
    elif website['website'] == 'consigliodeuropait':
        scraper = ConsiglioDEuropaITScraper(driver, target_date)
    elif website['website'] == 'consiglioeuropeo':
        scraper = ConsiglioEuropeo(driver, target_date)
    elif website['website'] == 'cor':
        scraper = CORScraper(driver, target_date)
    elif website['website'] == 'cor_events':
        scraper = COREventScraper(driver, target_date)
    elif website['website'] == 'cpmr':
        scraper = CPMRScraper(driver, target_date)
    elif website['website'] == 'eea':
        scraper = EEAScraper(driver, target_date)
    elif website['website'] == 'earlall':
        scraper = EarlAllScraper(driver, target_date)
    elif website['website'] == 'earlall_eventi':
        scraper = EarlAllEventScraper(driver, target_date)
    elif website['website'] == 'ecgeneric':
        scraper = ECGenericScraper(driver, target_date)
    elif website['website'] == 'ecitalia':
        scraper = ECItaliaScraper(driver, target_date)
    elif website['website'] == 'eib':
        scraper = EIBScraper(driver, target_date)
    elif website['website'] == 'eib_eventi':
        scraper = EIBEventScraper(driver, target_date)
    elif website['website'] == 'eif':
        scraper = EIFScraper(driver, target_date)
    elif website['website'] == 'eit':
        scraper = EITScraper(driver, target_date)
    elif website['website'] == 'eit_eventi':
        scraper = EITEventScraper(driver, target_date)
    elif website['website'] == 'enicbcmed':
        scraper = EniCbcMedScraper(driver, target_date)
    #This does not work
    elif website['website'] == 'espon':
        scraper = EsponScraper(driver, target_date)
    elif website['website'] == 'eucommission':
        scraper = EUCommissionScraper(driver, target_date)
    elif website['website'] == 'euparliament':
        scraper = EUParliamentScraper(driver, target_date)
    elif website['website'] == 'euregha':
        scraper = EureghaScraper(driver, target_date)
    elif website['website'] == 'europeanagency':
        scraper = EuropeanAgencyScraper(driver, target_date)
    elif website['website'] == 'eurostat':
        scraper = EurostatScraper(driver, target_date)
    elif website['website'] == 'eusalp':
        scraper = EusalpScraper(driver, target_date)
    elif website['website'] == 'imi':
        scraper = IMIScraper(driver, target_date)
    elif website['website'] == 'interreg':
        scraper = InterregScraper(driver, target_date)
    elif website['website'] == 'interreg_eventi':
        scraper = InterregEventScraper(driver, target_date)
    elif website['website'] == 'jrc':
        scraper = JRCScraper(driver, target_date)
    elif website['website'] == 'jrc_eventi':
        scraper = JRCEventScraper(driver, target_date)
    elif website['website'] == 'promis':
        scraper = PromisScraper(driver, target_date)
    elif website['website'] == 'eceducation':
        scraper = ECEducationScraper(driver, target_date)
    elif website['website'] == 'ecoceans':
        scraper = ECOceansScraper(driver, target_date)
    elif website['website'] == 'ec_politicheregionali':
        scraper = ECRegionalPolicyScraper(driver, target_date)
    # I have to find a way to load the website
    #elif website['website'] == 'ec_politicheregionali_it':
    #    scraper = ECRegionalPolicyScraper(driver, target_date)
    elif website['website'] == 'ecrea':
        scraper = ECReaScraper(driver, target_date)
    else:
        pass

    df = scraper.scrape()

    # Here i need to put the source
    for id, article in df.iterrows():
        try:
            insert_articles(article['title'], article['pub_date'].strftime("%Y-%m-%d"), article['snippet'], article['url'], website['website'])
        except:
            insert_articles(article['title'], date(2021,12,31).strftime("%Y-%m-%d"), article['snippet'], article['url'], website['website'])

driver.close()
