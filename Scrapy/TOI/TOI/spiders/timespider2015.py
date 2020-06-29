import scrapy

class Spider(scrapy.Spider):
    name = "toi_spider"
    start_urls = ["https://timesofindia.indiatimes.com/2009/1/1/archivelist/year-2009,month-1,starttime-39814.cms"]

    def numberofdays(self, month, year):

        x = int(month)
        y = int(year)
        numberdays = 0
        if(x == 1 or x == 3 or x == 5 or x == 7 or x == 8 or x == 10 or x == 12) :
            numberdays = 31
        elif (x == 2):
            if (y % 4 == 0):
                numberdays = 29
            else:
                numberdays = 28
        else:
            numberdays = 30
        return numberdays

    def parse(self, response):

        link = Spider.start_urls[0]
        pos1 = link.find("starttime-")
        pos2 = link.find(".cms")
        pos3 = link.find("year-")
        pos4 = link.find(",month-")

        monthid = int(link[pos1 + 10:pos2])
        year = int(link[pos3 + 5: pos4])
        # month = int(link[pos4 + 7: pos1 - 1])

        for month in range(1, 13):

            totaldays = self.numberofdays(month, year)

            for i in range(1, totaldays+1):
                metadatarequired = dict()
                date = str(i) + "/" + str(month) + "/" + str(year)
                metadatarequired["Date"] = date
                linkappendable = 'https://timesofindia.indiatimes.com/'+str(year)+"/"+str(month)+"/"+str(i)+"/archivelist/year-"+str(year)+",month-"+str(month)+",starttime-"+str(monthid+i-1)+".cms"
                req = scrapy.Request(linkappendable, callback=self.parse1, dont_filter=True)
                req.meta["item"] = metadatarequired
                yield req

            monthid = monthid + totaldays

    def parse1(self, response1):

        metadatarequired = response1.meta['item']
        all_links = response1.xpath("//span[@style='font-family:arial ;font-size:12;color: #006699']").css("a::attr(href)").extract()

        for href in all_links:
            metadatarequired["URL"] = href
            url = response1.urljoin(href)
            req = scrapy.Request(url, callback=self.parse2, dont_filter=True)
            req.meta["item"] = metadatarequired
            yield req

    def parse2(self, response2):

        metadatarequired = response2.meta['item']

        date = metadatarequired["Date"]
        linkurl = metadatarequired["URL"]
        pos = [j for j in range(len(linkurl)) if linkurl.startswith("/", j)]
        section = linkurl[pos[3] + 1:pos[4]]

        headline = response2.css('h1::text').extract_first()
        if(headline is None):
            headline = response2.css("div::attr(data-arttitle)").extract_first()

        headline = headline.replace(";", ",")

        article_content = response2.xpath("//div[@class='Normal']").css("::text").extract_first()
        if( article_content is None ):
            article_content = response2.xpath("//div[@class='_3WlLe clearfix  ']").css("::text").extract()
        else:
            article_content = response2.xpath("//div[@class='Normal']").css("::text").extract()
        article = ""
        for art in range(len(article_content)):
            article = article + article_content[art]

        article = article.replace(";", ",")

        article_dict = dict()
        article_dict['Headline'] = str(headline)
        article_dict["Date"] = str(date)
        article_dict["Section"] = str(section)
        article_dict["Article"] = str(article)

        if ( headline is not None):
            yield article_dict












