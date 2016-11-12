import scrapy
import urllib
import os


class AuthorSpider(scrapy.Spider):
    name = 'yami'

    start_urls = ['http://www.yamibuy.com/cn/category.php?id=101&brands=&brand_name_list=&sort_order=0&sort_by=3&page=1']

    def parse(self, response):
        print("***Catalog page: " + response.url)
        # get into the item page
        for href in response.xpath('//div[@class="items"]/div/div/a[contains(@href,"goods.php")]/@href').extract():
            url = response.urljoin(href)
            print("***Parse item page " + url)
            yield scrapy.Request(url,
                                 callback=self.parse_item)

        # follow pagination links
        page = int(response.url[-1])
        next_page_disable = response.xpath('//a[@class="disabled-btn" and @id="next-page"]').extract_first()
        if next_page_disable is None:
            next_page = response.url[:-1] + str(page+1)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_item(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        name = extract_with_xpath('//h1[@class="item-name"]/text()')
        itemImage = extract_with_xpath('//div[@class="thumb-cont"]/img/@src')
        itemInfoImage = extract_with_xpath('//img[contains(@src,"itemdescription")]/@src')

        yield {
            'name': name,
            'itemImage': itemImage,
            'itemInfoImage': itemInfoImage,
        }

        image_name = os.path.join("images", name.encode('utf_8')+".jpg")
        image_info_name = os.path.join("images", name.encode('utf_8')+"_info.jpg")
        urllib.urlretrieve(itemImage, image_name)
        urllib.urlretrieve(itemInfoImage, image_info_name)