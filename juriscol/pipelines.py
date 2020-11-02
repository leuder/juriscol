# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class JuriscolPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    collection_name = 'sentence'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'juriscol')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        def process_magistrate(item, magistrate, rol):
            magistrate_list = item.get(magistrate)
            if magistrate_list:
                del item[magistrate]
                return [{"name": name, "rol": rol} for name in magistrate_list]
            else:
                return []
        item["_id"] = f'{item["source"]}_{item["sentence_id"]}'
        # judicature
        magistrate = process_magistrate(item, "magistrate", 'PONENTE')
        magistrate_av = process_magistrate(
            item, "magistrate_av", 'ACLARACIÓN DE VOTO')
        magistrate_apv = process_magistrate(
            item, "magistrate_apv", 'ACLARACIÓN PARCIAL DE VOTO')
        magistrate_sv = process_magistrate(
            item, "magistrate_sv", 'SALVAMENTO DE VOTO')
        magistrate_spv = process_magistrate(
            item, "magistrate_spv", 'SALVAMENTO PARCIAL DE VOTO')
        item["judicature"] = magistrate + \
            magistrate_av + magistrate_apv + magistrate_sv + magistrate_spv
        # Participants
        participants = []
        if item.get("plaintiff"):
            participants.append(
                {"name": item.get("plaintiff"), "role": "plaintiff".upper()})
            del item["plaintiff"]

        if item.get("defendant"):
            participants.append(
                {"name": item.get("defendant"), "role": "defendant".upper()})
            del item["defendant"]

        if len(participants):
            item["participants"] = participants

        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())

        return item
