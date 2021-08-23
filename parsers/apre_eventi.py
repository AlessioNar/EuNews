from scraper import Scraper

class ApreEventScraper(Scraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.cookie_xpath = '//button[@class="iubenda-cs-reject-btn iubenda-cs-btn-primary"]'
        self.container_xpath = '//div[@id="more-events"]'
        self.url = 'https://apre.it/eventi/'

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
        list_item = soup.find_all('div', {'class':'single--event-content'})
        for item in list_item:
            title = item.h3.text.strip()
            url_item = item.find('div',{'class':'scopri'})
            url = url_item.a['href']
            snippet_item = item.find('div', {'class':'desc-eventi'})
            snippet = snippet_item.p.next_sibling.text.strip()
            titles.append(title)
            urls.append(url)
            snippets.append(snippet)
        list_item = soup.find_all('div', {'class':'single--event-image'})
        for item in list_item:
            pub_date = item.text.strip()
            pub_date = self.std_date(pub_date)
            pub_dates.append(pub_date)

        return titles, pub_dates, snippets, urls
