import scrapy
import os


class QuotesSpider(scrapy.Spider):
    name = "crawl_cs"

    def start_requests(self):
        urls = ['http://bulletin.iit.edu/search/?P=CS%20'+str(x) for x in range(100, 700)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1][-3:]
        filename = f'crawler/cs_courses/{page}.html'
        success = (len(response.css('p.noindent::text').getall()) != 0)
        if success:
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

class CSCourses(scrapy.Spider):
    name = 'cs_course'
    # start_urls = ['http://bulletin.iit.edu/undergraduate/courses/cs/']
    start_urls = [f'file://{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/cs_courses/{c}' for c in os.listdir('crawler/cs_courses')]

    def parse(self, response):

        classes = response.css('div.searchresults')
        try:
            yield {
                'code': 'CS'+classes.css('h2::text').get().split('\n')[0].strip()[-3:],
                'title': classes.css('h2::text').get().split('\n')[1].strip(),
                'link': 'http://bulletin.iit.edu/search/?P=CS%20'+ classes.css('h2::text').get().split('\n')[0].strip()[-3:],
                'description': classes.css('p.noindent::text').get().replace("\n", ""),
                'credits': classes.css('span::text').extract()[2],
                'prerequisites:': ['CS' + x.strip()[-3:] for x in classes.css('div.noindent.courseblockattr').css('a::text').getall()]
            }
        except:
            yield {
                'code': classes.css('div.noindent.coursecode::text').get(),
                'title': classes.css('strong::text').get(),
                'link': 'http://bulletin.iit.edu/search/?P=CS%20'+ classes.css('div.noindent.coursecode::text').get()[-3:],
                'description': classes.css('p.noindent::text').get().replace("\n", ""),
                'credits': classes.css('span::text').extract()[2],
                'prerequisites:': ['CS' + x.strip()[-3:] for x in classes.css('div.noindent.courseblockattr').css('a::text').getall()]
            }               
