import scrapy

class Spider(scrapy.Spider):
    name = "article_spider"


    start_urls = ['https://www.thehindu.com/archive/web/2009/08/15/']

    def parse(self, response):
        all_divs = response.css('.tpaper-container')
        all_sections = all_divs.css("section")
        topics = ['bengaluru', 'chennai', 'international', 'thiruvananthapuram', 'vijayawada', 'visakhapatnam',
                  'national', 'andhra pradesh',
                  'karnataka', 'kerala', 'tamil nadu', 'other states', 'coimbatore', 'delhi', 'hyderabad']

        for sect in all_sections:
            temp = sect.css("h2::attr(id)").extract_first()
            if temp in topics:
                arc_list = sect.css(".archive-list")
                all_headlines = arc_list.css("li")
                for hd in all_headlines:
                    child_links = hd.css('a::attr(href)')
                    for clk in child_links:
                        url = clk.get()
                        ret_dict = {'Headline': hd.css('a::text').get()}
                        req = scrapy.Request(url, callback=self.parse2, dont_filter=True)
                        req.meta['item'] = ret_dict
                        yield req

    def parse2(self, response2):
        ret_dict = response2.meta['item']
        date = response2.css('span[class="blue-color ksl-time-stamp"]')
        date = date.css('none::text').get()
        txt = response2.css('.article')
        cont = txt.css('div::attr(id)').get()
        txt = txt.css('div[id='+cont+']')
        content = ""
        txt = txt.css('p::text')
        for t in txt:
            content = content + " " + t.get()
        ret_dict['Date'] = date.replace('\n','')
        ret_dict['Text'] = content
        yield ret_dict
