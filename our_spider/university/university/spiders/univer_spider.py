import scrapy


class UniverSpider(scrapy.Spider):
    name = 'postupi_online'
    start_urls = ['https://spb.postupi.online/programmy-obucheniya/bakalavr/?sort_type=1&page_num=2']

    def parse(self, response, **kwargs):
        for link in response.css('ul.list-unstyled a.list__img::attr(href)'):
            yield response.follow(link, callback=self.parse_info)

        for i in range(1, 61):
            next_page = f"https://spb.postupi.online/programmy-obucheniya/bakalavr/?sort_type=1&page_num={i}"
            yield response.follow(next_page, callback=self.parse)

    def parse_info(self, response):

        # try:
        #     code = response.css('p.bg-nd__pre a::text').getall()[0].split(' ')[-1][1:-1]
        # except IndexError:
        #     code = ''

        try:
            universe = response.css('a.violet-link-nd::text').get()
            if ',' in universe:
                universe = universe.replace(u'\xa0', u'')
                print(universe[:-1])
        except IndexError:
            universe = ''

        try:
            name = ' '.join(response.css('p.bg-nd__pre a::text').getall()[0].split(' ')[0:-1])
        except IndexError:
            name = ''

        try:
            details = response.css('div.descr-max li::text').getall()
            details_new = []
            for i in details:
                one = i.replace(u'\xa0', u'')
                two = one.replace(u';', u'')
                three = two.replace(u'.', u'')
                four = three.replace(u' и др.', u'')
                details_new.append(four)
        except IndexError:
            details = []

        # try:
        #     specialnost = response.css('div.bg-nd__main h1::text').get().split(':')[0]
        # except IndexError:
        #     specialnost = ''

        yield {
            # code: [universe, name, specialnost, details],
            name: [universe, name, details]
        }
