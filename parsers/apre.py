from scraper import Scraper

class ApreScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//button[@class="iubenda-cs-reject-btn iubenda-cs-btn-primary"]'
        self.container_xpath = '//main[@class="site-main"]'
        self.url = 'https://apre.it/news/'

    def cookies_removal(self):
        try:
            cookies = driver.find_element_by_xpath(self.cookie_xpath)
            cookies.click()
            time.sleep(1)
        except:
            print('Cookies already set')

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()
        soup = self.extract_html()

        # Parse html
        list_item = soup.find_all('h2', {'class':'entry-title'})
        for item in list_item:
            title = item.text.strip()
            url = item.a['href']
            titles.append(title)
            urls.append(url)
        list_item = soup.find_all('span', {'class':'published'})
        for item in list_item:
            pub_date = item.text.strip()
            pub_date = self.std_date(pub_date)
            pub_dates.append(pub_date)
        list_item = soup.find_all('div', {'id':'bottom-blog'})
        for item in list_item:
            snippet = item.text.strip()
            snippets.append(snippet)

        return titles, pub_dates, snippets, urls
