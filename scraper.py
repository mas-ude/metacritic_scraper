## Metacritic Scraper

import urllib2
import lxml.html
import csv


# This is where we will output to
output_file = open('metacritic.csv', 'wb')
csv_writer = csv.DictWriter(output_file, fieldnames=["user_score", 
        "publisher", "title", "url", "genre", "score", "release"])
csv_writer.writeheader()


page = 0
while True:
    url = "http://www.metacritic.com/browse/games/release-date/available/pc/name?hardware=all&view=detailed&page=%s" + str(page)
    request = urllib2.Request(url, headers={"User-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"})
    html = urllib2.urlopen(request).read()
    root = lxml.html.fromstring(html)

    # Have we reached the end of the search results already?
    # If we have, we'll see the end marker. If not, the xpath 
    # selects an empty list.
    expected_end_marker = root.xpath("//div[@class='module products_module list_product_summaries_module ']/div/div/p[@class='no_data']/text()")
    try:
        if expected_end_marker[0] == "No Results Found":
            break
    except Exception, e:
        pass

    # No, not done yet. Continue with products
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
        if len(user_score) != 1 or user_score[0] == 'tbd':
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

        #scraperwiki.sqlite.save(unique_keys=['title','url','release','genre','publisher'], data=data)
        #print data

        csv_writer.writerow(data)

    # Do the next page of results
    page += 1

