# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class JumiadzCrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Cast Price to Float
        price = adapter.get("price")
        if price:
            price = int(price.replace("DA",""))
            adapter['price'] = price
            
        # Cast Rating Count to Integer
        rating_count = adapter.get("rating_count")
        if rating_count:
            rating_count = int(rating_count.split(" ")[0])
            adapter['rating_count'] = rating_count
        
        return item
    