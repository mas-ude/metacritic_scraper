# Metacritic Scraper
import scraperwiki
import lxml.html
import re

#types = ['0','1','2','3','4','5','6','7','8','9','10']
types = range(0,1)
for type in types:
    url = "http://www.metacritic.com/browse/games/release-date/available/pc/name?hardware=all&view=detailed&page=%s" % str(type)
    html = scraperwiki.scrape(url, user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1")
    root = lxml.html.fromstring(html)
    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")
    for product in products:
        data = {}
        data['title'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/text()")[0])
        data['url'] = str(product.xpath("div/div/div/div[@class='main_stats']/div[@class='basic_stat product_title']/h3[@class='product_title']/a/@href")[0])

        product_release = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat release_date']/span[@class='data']/text()")
        if len(product_release) != 1:
            data['release'] = ''
        else:
            data['release'] = str(product_release[0])

        genre = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat genre']/span[@class='data']/text()")
        if len(genre) != 1:
            data['genre'] = ''
        else:
            genre = str(genre[0]).replace('\n', '').replace('\r', '').replace('\t','')
            data['genre'] = genre

        user_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[2]/text()")
        if len(user_score) != 1or user_score[0] == 'tbd':
            data['user_score'] = ''
        else:
            data['user_score'] = str(user_score[0])


        product_publisher = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat publisher']/span[@class='data']/text()")
        if len(product_publisher) != 1:
            data['publisher'] = ''
        else:
            data['publisher'] = str(product_publisher[0])


        product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/span/text()")
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = ''
        else:
            data['score'] = product_score[0]

        scraperwiki.sqlite.save(unique_keys=['title','url','release','genre','publisher'], data=data)
