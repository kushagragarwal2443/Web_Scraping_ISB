import scrapy

class Spider(scrapy.Spider):
    name = "monthly_spider"

    allowed_domains = ["thehindu.com/archive/"]

    start_urls = ['https://www.thehindu.com/archive/web/2019/12/']

    def parse(self, response):
        tb = response.css('.table-responsive')
        tb = tb.css('a[class="ui-state-default"]::attr(href)')
        for t in tb:
            request = scrapy.Request(t.get(), callback = self.parse1, dont_filter=True)
            request.meta['main_item'] = {}
            yield request


    def parse1(self, response):
        main_dict = response.meta['main_item']
        all_divs = response.css('.tpaper-container')
        all_sections = all_divs.css("section")
        topics = {'national':1, 'andhra pradesh':1, 'industry':1, 'economy':1, 'markets':1, 'business':1, 'kolkata':1,
                  'karnataka':1, 'kerala':1, 'tamil nadu':1, 'other states':1, 'delhi':1, 'telangana':1}

        for sect in all_sections:
            temp = sect.css("h2::attr(id)").extract_first()
            if temp in topics.keys():
                arc_list = sect.css(".archive-list")
                all_headlines = arc_list.css("li")
                for hd in all_headlines:
                    child_links = hd.css('a::attr(href)')
                    for clk in child_links:
                        url = clk.get()
                        req = scrapy.Request(url, callback=self.parse2, dont_filter=True)
                        req.meta['item'] = main_dict
                        req.meta['category'] = temp
                        yield req

    def parse2(self, response2):
        main_dict = response2.meta['item']
        headline = response2.css('div[class="article"]')
        headline = headline.css('h1::text').get()

        date = response2.css('span[class="blue-color ksl-time-stamp"]')
        date = date.css('none::text').get()
        txt = response2.css('.article')
        cont = txt.css('div::attr(id)').get()
        txt = txt.css('div[id='+cont+']')
        content = ""
        txt = txt.css('p::text')
        for t in txt:
            content = content + " " + t.get()
            if len(content) >= 200:
                break
        main_dict['Date'] = date.replace('\n','')
        main_dict['Category'] = response2.meta['category']
        main_dict['Headline'] = headline.replace('\n','')
        main_dict['Text'] = content
        yield main_dict