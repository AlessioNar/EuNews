from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import bs4

def get_article_list(url, source):
    driver = webdriver.Firefox()
    driver.get(url)
    sleep(3)

    if source == 'consigliodeuropait':
        article_containers = driver.find_elements_by_xpath('//div[@class="newsroom "]')[0]
    elif source == 'eucommission':
        article_containers = driver.find_elements_by_xpath('//section[@id="news-block"]')[0]
    elif source == 'eusalp':
        article_containers = driver.find_elements_by_xpath('//div[@class="view-content"]')[0]
    elif source == 'areflh':
        article_containers = driver.find_elements_by_xpath('//div[@class="uk-container"]')[1]
    elif source == 'eurostat':
        article_containers = driver.find_elements_by_xpath('//ul[@class="product-list"]')[0]
    elif source == 'imi':
        article_containers = driver.find_elements_by_xpath('//div[@class="view-grouping-content info-box light-grey-bg"]')[0]
    elif source == 'eib':
        article_containers = driver.find_elements_by_xpath('//div[@class="search-filter__results row card-row-items"]')[0]
    elif source == 'euparliament':
        article_containers = driver.find_elements_by_xpath('//div[@class="ep_gridrow ep-o_productlist"]')[0]
    elif source == 'eif':
        article_containers = driver.find_elements_by_xpath('//div[@class="span7 border_left news_centre_ news_centre_press_releases_"]')[0]
    elif source == 'consiglioeuropeo':
        cookies = driver.find_elements_by_xpath('//span[@id="reject_cookies"]')[0]
        cookies.click()
        article_containers = driver.find_elements_by_xpath('//div[@class="col-md-9 council-flexify-item pull-right"]')[0]
    elif source == 'esma':
        article_containers = driver.find_elements_by_xpath('//table[@class="views-view-grid cols-2"]')[0]
    elif source == 'horizon2020':
        article_containers = driver.find_elements_by_xpath('//ul[@class="listing listing--teaser"]')[0]
    elif source == 'easme':
        article_containers = driver.find_elements_by_xpath('//ul[@class="ecl-listing ecl-formatter-listing-plugin-style"]')[0]
    elif source == 'eit':
        article_containers = driver.find_elements_by_xpath('//div[@class="news eit-list"]')[0]
    elif source == 'cor':
        article_containers = driver.find_elements_by_xpath('//div[@class="cbq-layout-main"]')[0]
    elif source == 'parlamento_europeo_thinktank_eventi':
        article_containers = driver.find_elements_by_xpath('//div[@class="listcontent nobackground"]')[0]
    elif source == 'urbact':
        article_containers = driver.find_elements_by_xpath('//div[@class="panel-pane pane-views-panes pane-urbact-articles-article-list-news"]')[0]
    elif source == 'interact':
        article_containers = driver.find_elements_by_xpath('//div[@class="view view-news view-id-news view-display-id-default view-dom-id-9ca0c5368c92bd6815d065517c203a8b jquery-once-1-processed"]')[0]
    elif source == 'europeanagency':
        article_containers = driver.find_elements_by_xpath('//div[@class="view-content"]')[0]
    elif source == 'enicbcmed':
        article_containers = driver.find_elements_by_xpath('//div[@class="block-items"]')[0]
    elif source == 'apre':
        article_containers = driver.find_elements_by_xpath('//main[@class="site-main"]')[0]
    elif source == 'cpmr':
        article_containers = driver.find_elements_by_xpath('//div[@id="posts-container"]')[0]
    elif source == 'earlall':
        article_containers = driver.find_element_by_xpath('//div[@id="content-full"]')
    elif source == 'eea':
        article_containers = driver.find_element_by_xpath('//div[@class="entries"]')
    elif source == 'espon':
        article_containers = driver.find_elements_by_xpath('//ul[@class="recent-posts"]')[3]
    elif source == 'euregha':
        article_containers = driver.find_elements_by_xpath('//div[@class="et_pb_blog_grid clearfix  et_pb_text_align_center"]')[0]
    elif source == 'interreg':
        article_containers = driver.find_elements_by_xpath('//div[@class="content-area"]')[0]
    elif source == 'jrc':
        article_containers = driver.find_elements_by_xpath('//div[@class="block block-system panel panel-default clearfix"]')[0]
    elif source == 'promis':
        article_containers = driver.find_element_by_xpath('//div[@id="boxNotizieArchivio"]')
    else:
        print("There is not yet a retrieval method for this website")
        driver.close()
        return 1
    article_containers = article_containers.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(article_containers, 'lxml')
    driver.close()

    return soup
