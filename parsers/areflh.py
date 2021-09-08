from scraper import Scraper
import bs4
import re

class AreflhScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//button[@class="iubenda-cs-reject-btn iubenda-cs-btn-primary"]'
        self.container_xpath = '//div[@class="uk-container"]'
        self.url = 'http://www.areflh.org/index.php?lang=en'

    def cookies_removal(self):
        try:
            cookies = driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)
        except:
            print('Cookies already set')

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def extract_html(self):
        container = self.driver.find_elements_by_xpath(self.container_xpath)[1]
        container = container.get_attribute('innerHTML')
        soup = bs4.BeautifulSoup(container, 'lxml')
        return soup

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()
        soup = self.extract_html()

        # Parse html
        list_item = soup.find_all("h3", {"class": "el-title uk-card-title uk-margin-top uk-margin-remove-bottom"})
        for item in list_item:
            title = item.text.strip()
            titles.append(title)

        list_item = soup.find_all("a", {"class": "el-item uk-card uk-card-default uk-card-hover uk-link-toggle uk-display-block"})
        for item in list_item:
            url = 'https://www.areflh.org' + item['href']
            urls.append(url)

        list_item = soup.find_all("div", {"class": "el-meta uk-text-meta uk-margin-top"})
        for item in list_item:
            pub_date = re.sub('Publié le', '', item.text).strip()
            pub_date = self.std_date(pub_date)    
            pub_dates.append(pub_date)

        list_item = soup.find_all("div", {"class": "el-content uk-panel uk-margin-top"})
        for item in list_item:
            if item.p:
                snippet = item.p.text
            else:
                snippet = item.div.text
            snippets.append(snippet)

        return titles, pub_dates, snippets, urls
