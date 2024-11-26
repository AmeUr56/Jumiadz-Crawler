import scrapy
from ..items import ProductItem

class JumiadzSpiderSpider(scrapy.Spider):
    name = "jumiadz_spider"
    start_urls = ["https://www.jumia.com.dz/"]

    HEADERS = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    def parse(self, response):
        # Get All Categories URLs
        categories = response.xpath("//div[@id='jm']//main[@class='has-b2top']//div[@class='flyout']/a/@href").getall()

        for category in categories:
            # Construct Each Category URL
            if not category.startswith("http"):
                category = self.start_urls[0] + category
                
            # Redirect To Each Category Page
            yield scrapy.Request(category,callback=self.parse_category,headers=self.HEADERS)
        
    def parse_category(self,response):
        # Get all Products
        products = response.xpath("//div[@id='jm']//main[contains(@class,'has-b2top')]//section[@class='card -fh']/div[@data-catalog='true']//article")
        
        for product in products:
            # Get & Construct Each Product URL
            product_url = product.xpath("./a/@href").get()
            if not product_url.startswith("http"):
                product_url = self.start_urls[0] + product_url
            
            # Redirect To Each Category Page
            yield scrapy.Request(product_url,callback=self.parse_product,headers=self.HEADERS)
            
        # Redirect Next Pages
        next_page_url = response.xpath("//div[@id='jm']//main[contains(@class,'has-b2top')]//div[@class='-pvs col12']//div[@class='pg-w -ptm -pbxl']/a[@aria-label='Page suivante']/@href").get()

        if next_page_url:
            if not next_page_url.startswith("http"):
                next_page_url = self.start_urls[0] + next_page_url
            
            yield scrapy.Request(next_page_url,callback=self.parse_category,headers=self.HEADERS)

    def parse_product(self,response):
        # Initialize ProductItem
        product_item = ProductItem()
        
        # Extract Product Informations
        product_item['product_id'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='card aim -mtm -fs16']/div[@class='row -pas']//article[.//h2[text()='Descriptif technique']]//ul/li[1]/text()").get() 
        product_item['url'] = response.url
        product_item['category'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//div[@class='brcbs col16 -pts -pbm']/a[2]/text()").get()
        product_item['name'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='col12 -df -d-co']//div[@class='col10']//h1/text()").get()
        product_item['brand'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='col12 -df -d-co']//div[@class='col10']//div[@class='-phs']//div[@class='-pvxs']/a/text()").get()
        product_item['price'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='col12 -df -d-co']//div[@class='col10']//div[@class='-phs']//div[@class='-hr -mtxs -pvs']/div[contains(@class,'df -i-ctr -fw-w')]//span/text()").get()
        product_item['rating'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='card aim -mtm']//div[@class='col4 -phm']//div[@class='-fsh0 -bg-gy05 -df -d-co -i-ctr -rad4 -pam']//span/text()").get()
        product_item['rating_count'] = response.xpath("//div[@id='jm']//main[contains(@class,'-pvs')]//section[@class='card aim -mtm']//div[@class='col4 -phm']//div[@class='-fsh0 -bg-gy05 -df -d-co -i-ctr -rad4 -pam']//p/text()").get() 
       
        # if any field other than 'url' is empty do not yield the item 
        #if not (product_item['product_id'] or product_item['category'] or product_item['name'] or product_item['brand'] or product_item['price'] or product_item['rating'] or product_item['rating_count']):
        #    return
       
        yield product_item