from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from websites import *

driver = webdriver.Firefox()

## I should have included all websites

url = 'https://urbact.eu/urbact-news'
date = datetime.date(2021,5,10)

driver.get(url)

urbact(url, driver, date)

final_df = pd.DataFrame()
