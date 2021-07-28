from selenium import webdriver
from datetime import date

from parsers.apre import ApreScraper
from parsers.areflh import AreflhScraper
from parsers.consigliodeuropait import ConsiglioDEuropaITScraper
from parsers.consiglioeuropeo import ConsiglioEuropeo
from parsers.cor import CORScraper
from parsers.cpmr import CPMRScraper
from parsers.earlall import EarlAllScraper
from parsers.eea import EEAScraper
from parsers.eib import EIBScraper
from parsers.eif import EIFScraper
from parsers.eit import EITScraper
from parsers.enicbcmed import EniCbcMedScraper
from parsers.espon import EsponScraper
from parsers.eucommission import EUCommissionScraper
from parsers.euparliament import EUParliamentScraper
from parsers.euregha import EureghaScraper
from parsers.europeanagency import EuropeanAgencyScraper


from db_operations import *

create_table()
target_date = date(2021, 6, 20)
driver = webdriver.Firefox()
#test = ApreScraper(driver, target_date)
#test = AreflhScraper(driver, target_date)

#test = ConsiglioDEuropaITScraper(driver, target_date)
#test = ConsiglioEuropeo(driver, target_date)
#test = CORScraper(driver, target_date)
#test = CPMRScraper(driver, target_date)

# To check
#test = EEAScraper(driver, target_date)

#test = EarlAllScraper(driver, target_date)
#test = EIBScraper(driver, target_date)
#test = EIFScraper(driver, target_date)
#test = EITScraper(driver, target_date)
#test = EniCbcMedScraper(driver, target_date)

#This does not work
#test = EsponScraper(driver, target_date)

#test = EUCommissionScraper(driver, target_date)
#test = EUParliamentScraper(driver, target_date)
#test = EureghaScraper(driver, target_date)
test = EuropeanAgencyScraper(driver, target_date)

df = test.scrape()
for id, article in df.iterrows():
    insert_articles(article['title'], article['pub_date'].strftime("%Y-%m-%d"), article['snippet'], article['url'])

driver.close()

#print(df)
#print(df['pub_date'])
