import pymssql
import datetime
import re


class MSSQLPipeline(object):

    def __init__(self):

        self.con = pymssql.connect('Adnan', '', '', 'BeBranded_DB')
        self.cur = self.con.cursor()
        self.cur.execute('select Bid from Brand where name like %s', '%Khaadi%')
        one = self.cur.fetchone()
        if one:
            self.brand_id = one[0]

    def process_item(self, item, spider):
        query = "insert into Product values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        tpl = self.get_tuple(item)
        if tpl:
            self.cur.execute(query, tpl)
            self.con.commit()
            self.images_insertion(item)

        return item

    def images_insertion(self, item):
        record_list = list()
        self.cur.execute('SELECT TOP 1 Pid  FROM Product ORDER BY Pid DESC')
        last_rec = self.cur.fetchone()
        if last_rec:
            for i in item['image_url']:
                record_list.append((last_rec[0], i))
            self.cur.executemany('insert into Images values(%s, %s)', record_list)
            self.con.commit()

    def parse_categories(self, cate):

        if re.findall('[A-z]\d+[A-Z]?', cate):
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Unistiched'))

        elif 'Kurta Pajama' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Kurta Pajama'))

        elif 'Kurta' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Kurta'))

        elif 'Blouse' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Blouse'))

        elif 'Pant' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Pant'))

        elif 'Shalwar' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Shalwar'))

        elif 'Tights' in cate:
            self.cur.execute('select SbCatId from SubCategory where CatId=%s and Name=%s', ('2', 'Tights'))
        try:
            subCate = self.cur.fetchone()
            if subCate:
                return subCate[0]
        except:
            Exception.message

    def get_SKU(self, item):
        sku = re.match('Product\scode:\s([\w\-]+)', item)
        if sku:
            return sku.group(1)

    def get_tuple(self, item):
        sub_cate = self.parse_categories(item['category'])
        if sub_cate:
            attribute_tuple = list()
            attribute_tuple.append(self.brand_id)
            attribute_tuple.append(sub_cate)
            attribute_tuple.append(item['title'])
            attribute_tuple.append(self.get_SKU(item['detail']))
            attribute_tuple.append(item['regular_price'])
            attribute_tuple.append(item['special_price'])
            attribute_tuple.append(item['description'] + '\n\n\n\n' +item['detail'])
            attribute_tuple.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            attribute_tuple.append(item['product_url'])

            return tuple(attribute_tuple)

    def __del__(self):
        self.con.close()
