from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def get_article_list(url, source):
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(3)

    if source == 'consigliodeuropait':
        article_containers = driver.find_elements_by_xpath('//div[@class="newsroom "]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    if source == 'eucommission':
        article_containers = driver.find_elements_by_xpath('//section[@id="news-block"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    if source == 'consiglioeuropeo':
        cookies = driver.find_elements_by_xpath('//span[@id="reject_cookies"]')[0]
        cookies.click()
        article_containers = driver.find_elements_by_xpath('//div[@class="col-md-9 council-flexify-item pull-right"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')
    if source == 'esma':
        article_containers = driver.find_elements_by_xpath('//table[@class="views-view-grid cols-2"]')[0]
        article_containers = article_containers.get_attribute('innerHTML')

    driver.close()

    return article_containers
