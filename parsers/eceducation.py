from scraper import Scraper, PaginatedScraper, EventScraper
import bs4
import time

class ECEducationScraper(PaginatedScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/education/news_en'
        self.container_xpath = '//section[@id="block-views-eat-news-page-news-block"]'
        self.next_xpath = '//a[@class="btn btn-secondary btn-show-more"]'

    def std_date(self, to_date):
        return self.std_date_day(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, pub_dates, snippets = self.initialize_lists()

        # Initialize variables for while
        is_paginated = True
        while is_paginated:
            soup = self.extract_html()
            soup = soup.div.find('div', {'class':'view-content'})
            list_item = soup.find_all('div',{'class':'views-field views-field-title'})
            for item in list_item:
                title = item.text.strip()
                url = 'https://ec.europa.eu' + item.a['href']
                snippet = ''
                titles.append(title)
                urls.append(url)
                snippets.append(snippet)
            list_item = soup.find_all('span', {'class':'date-display-single'})
            for item in list_item:
                pub_date = item.text.strip()
                pub_date = self.std_date(pub_date)
                pub_dates.append(pub_date)

            if pub_dates[len(pub_dates) - 1] <= self.max_date:
                is_paginated = False
            else:
                self.turn_page()

        return titles, pub_dates, snippets, urls


class ECEducationEventScraper(EventScraper):

    def __init__(self, driver, max_date):
        self.driver = driver
        self.max_date = max_date
        self.url = 'https://ec.europa.eu/education/events_en'
        self.container_xpath = '//section[@id="block-views-eat-news-page-news-block"]'
        self.next_xpath = '//a[@class="btn btn-secondary btn-show-more"]'

    def cookies_removal(self):
        try:
            cookies = self.driver.find_element_by_xpath("//a[@class='cck-actions-button']")
            cookies.click()
            closecookies = self.driver.find_element_by_xpath("//a[@href='#close']")
            closecookies.click()
        except:
            print('no cookies')

    def std_date(self, to_date):
        return self.std_date_general(to_date)

    def parse(self):

        # initialize container lists
        titles, urls, start_dates, end_dates, snippets = self.initialize_lists()
        soup = self.extract_html()
        soup = soup.div

        # Parse html
        list_item = soup.find_all('article')
        for item in list_item:
            title = item.a.span.text.strip()
            url = 'https://digital-strategy.ec.europa.eu' + item.a['href']
            snippet = ''
            titles.append(title)
            urls.append(url)
            snippets.append(snippet)

        list_item = soup.find_all('div', {'class':'ecl-u-type-s ecl-u-type-color-grey-75 ecl-u-type-family-alt'})
        for item in list_item:
            dates = item.find_all('time')
            if len(dates) == 0:
                text = item.text.strip()
                text = text.split('|')[1].strip()
                if bool(re.search('to', text)):
                    splitted = text.split(' to ')
                    start_date = splitted[0]
                    end_date = splitted[1]
                else:
                    start_date = text
                    end_date = text
            elif len(dates) == 1:
                start_date = dates[0]['datetime']
                end_date = dates[0]['datetime']
            else:
                start_date = dates[0]['datetime']
                end_date = dates[1]['datetime']

            start_date = self.std_date(start_date)
            end_date = self.std_date(end_date)
            start_dates.append(start_date)
            end_dates.append(end_date)


        return titles, snippets, start_dates, end_dates, urls