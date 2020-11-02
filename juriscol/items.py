# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime

import scrapy
from itemloaders.processors import Identity, Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader
import re


def date_convert(value):
    return datetime.strptime(value, "%Y-%m-%d")


def magister_clean(value):
    return re.sub(r'^:', '', value).upper()


def participant_clean(value):
    return re.sub(r'^.', '', value).upper()


class StripFirstItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()


class JuriscolItem(scrapy.Item):
    _id = scrapy.Field()
    file_id = scrapy.Field()
    date = scrapy.Field(
        input_processor=MapCompose(str.strip, date_convert))
    sentence_id = scrapy.Field()
    magistrate = scrapy.Field(
        input_processor=MapCompose(str.strip, magister_clean),
        output_processor=Identity())
    magistrate_av = scrapy.Field(
        input_processor=MapCompose(str.strip, magister_clean),
        output_processor=Identity())
    magistrate_apv = scrapy.Field(
        input_processor=MapCompose(str.strip, magister_clean),
        output_processor=Identity())
    magistrate_sv = scrapy.Field(
        input_processor=MapCompose(str.strip, magister_clean),
        output_processor=Identity())
    magistrate_spv = scrapy.Field(
        input_processor=MapCompose(str.strip, magister_clean),
        output_processor=Identity())
    plaintiff = scrapy.Field(
        input_processor=MapCompose(participant_clean, str.strip))
    defendant = scrapy.Field(
        input_processor=MapCompose(participant_clean, str.strip))
    report_receipt_at = scrapy.Field(
        input_processor=MapCompose(str.strip, date_convert))
    report_receipt_at = scrapy.Field()
    topic = scrapy.Field()
    text = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    judicature = scrapy.Field(
        input_processor=Identity(), output_processor=Identity())
    participants = scrapy.Field(
        input_processor=Identity(), output_processor=Identity())
