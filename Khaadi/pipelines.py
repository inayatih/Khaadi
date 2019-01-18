# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class KhaadiPipeline(object):

    def process_item(self, item, spider):

        item['title'] = self.join_by_space(self.trim_spaces(item.get('title')))
        p = self.trim_spaces(item.get('regular_price'))
        price = self.get_prices(p)
        if isinstance(price, dict):
            item['regular_price'] = price.get('Regular Price:').encode('utf-8')
            item['special_price'] = price.get('Special Price:').encode('utf-8')
        else:
            item['regular_price'] = self.join_by_space(p)
            item['special_price'] = None
        item['description'] = self.join_by_newline(self.trim_spaces(item.get('description')))
        item['detail'] = self.join_by_space(self.trim_spaces(item.get('detail')))
        item['size'] = self.join_by_newline(self.trim_spaces(item.get('size')))
        item['category'] = self.join_by_space(self.trim_spaces(item.get('category')))
        item['product_url'] = item['product_url'][0]
        if not item.get("special_price"):
            item["special_price"] = item.get("regular_price")
        if item.get("special_price"):
            special_price = item["special_price"]
            special_price = int(float(special_price.replace('PKR ', '').replace(',', '')))
            item["special_price"] = special_price
            item["special_price"] = item.get("special_price") - int(item.get("special_price") * 0.1)

        return item

    def trim_spaces(self, value):

        if value:

            return [v.strip() for v in value if v.strip()]

    def get_prices(self, price):

        if 'Regular Price:' in price:
            return dict(zip(price[0::2], price[1::2]))
        return price

    def join_by_newline(self, value):

        if value:
            return '\n'.join(value).encode('utf-8')

    def join_by_space(self, value):
        if value:
            return ' '.join(value).encode('utf-8')




