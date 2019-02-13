import scrapy
import json

class TotoScraper(scrapy.Spider):
    # Use scrapy crawl toto, toto is the name here
    name = "toto"
    DATA_FILE_NAME = 'toto.txt'

    # Main function, start spider, can check this can work with multiple tread or not
    def start_requests(self):
        self.delete_file_contents(self.DATA_FILE_NAME)
        base_url = 'http://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx?'
        urls = self.generate_urls(base_url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    # Read querylinks.html to generate all html links to crawl
    def generate_urls(self, base_url):
        urls = []
        filename = 'querylinks.html'
        with open(filename, 'r') as f:
            lines = f.readlines()
            html_mark = 'option'
            for line in lines:
                if html_mark in line:
                    # The other way I will use is to split by 'sppl', will have more than one line. pending
                    urls.append(base_url + line[25: 50])
        return urls

    # Parse return into an json, didn't store all returns  
    def parse(self, response):
        try:
            page = response.url.split('/')[-2]
            with open(self.DATA_FILE_NAME, 'a') as f:
                crawler_data = {}
                # 4 Tables to store different information in html
                for content_table in response.css('.divSingleDraw table'):
                    draw_date = self.clean_html_text(content_table.css('.drawDate::text').get())
                    draw_number = self.clean_html_text(content_table.css('.drawNumber::text').get())
                    if draw_date is not None:
                        crawler_data['Draw date'] = draw_date
                    if draw_number is not None:
                        crawler_data['Draw number'] = draw_number
                    if content_table.css('.win1::text').get() is not None:
                        crawler_data['Winning numbers'] = [
                            self.clean_html_text(content_table.css('.win1::text').get()),
                            self.clean_html_text(content_table.css('.win2::text').get()),
                            self.clean_html_text(content_table.css('.win3::text').get()),
                            self.clean_html_text(content_table.css('.win4::text').get()),
                            self.clean_html_text(content_table.css('.win5::text').get()),
                            self.clean_html_text(content_table.css('.win6::text').get())
                        ]
                    if content_table.css('.additional::text').get() is not None:
                        crawler_data['Additional number'] = content_table.css('.additional::text').get()

                for winning_share in response.css('.divSingleDraw table.tableWinningShares tr'):
                    prize_group = self.clean_html_text(winning_share.css('td:first-child::text').get())
                    share_amount = self.clean_html_text(winning_share.css('td:nth-child(2)::text').get())
                    number_of_share = self.clean_html_text(winning_share.css('td:last-child::text').get())
                    # Condition checking to ignore those empty data and header row
                    if prize_group != '' and prize_group is not None and prize_group != 'Prize Group':
                        crawler_data[prize_group + ' prize'] = {
                            'Price group': prize_group,
                            'Share amount': share_amount,
                            'Number of shares': number_of_share
                        }
                f.write(json.dumps(crawler_data) + ',\n')
                f.close()
            self.log('saved file %s' % self.DATA_FILE_NAME)
        except:
            self.log_failed_urls(response.url)
            self.log('failed in url: %s' % response.url)
            pass

    def clean_html_text(self, value):
        if value is not None: 
            return value.replace('\r\n', '').strip()
    
    def log_failed_urls(self, url):
        filename = 'failedcrawllist.txt'
        with open(filename, 'a') as f:
            f.write(url + '\n')
            f.close()

    # Delete the contents of a file
    def delete_file_contents(self, path):
        open(path, 'w').close()
