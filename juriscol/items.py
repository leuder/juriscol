# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader

def date_convert(value):
    return datetime.strptime(value, "%Y-%m-%d").date()



class StripFirstItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)

class JuriscolItem(scrapy.Item):
    # define the fields for your item here like:
    demandante = scrapy.Field()
    demandado = scrapy.Field()
    expediente = scrapy.Field()
    fecha_sentencia = scrapy.Field(input_processor=MapCompose(str.strip, date_convert))
    magistrado = scrapy.Field()
    recibo_relatoria = scrapy.Field(input_processor=MapCompose(str.strip, date_convert))
    sentencia_id = scrapy.Field()
    tema = scrapy.Field()
    tipo = scrapy.Field()
    texto_sentencia = scrapy.Field()
    url = scrapy.Field()
    resolución = scrapy.Field()
