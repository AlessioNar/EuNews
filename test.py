from selenium import webdriver
from datetime import date

from parsers.apre import ApreScraper
from parsers.areflh import AreflhScraper
from parsers.consigliodeuropait import ConsiglioDEuropaITScraper
from parsers.consiglioeuropeo import ConsiglioEuropeo

target_date = date(2021, 6, 20)
driver = webdriver.Firefox()

#test = ApreScraper(driver, target_date)
#test = AreflhScraper(driver, target_date)
#test = ConsiglioDEuropaITScraper(driver, target_date)
test = ConsiglioEuropeo(driver, target_date)
df = test.scrape()

print(df)

driver.close()
