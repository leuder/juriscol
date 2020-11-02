import scrapy
from bs4 import BeautifulSoup
from juriscol.items import JuriscolItem, StripFirstItemLoader
from nlp_pos.transform import SpacyDoc

# Contendor sentencias=//tr[contains(@onmouseover, "uno(this") and position()>584]
# Expediente=./td/p[1]/strong[contains(.,"Expediente")]/following-sibling::text()[1]
# Fecha sentencia=./td/p[1]/strong[contains(.,"Fecha sentencia")]/following-sibling::text()[1]
# Sentencia=./td/p[1]/strong[contains(.,"Sentencia")]/following-sibling::a/text()
# URL Sentencia=./td/p[1]/strong[contains(.,"Sentencia")]/following-sibling::a/@href
# Magistrado Ponente=./td/p[1]/strong[contains(text(),"Magistrado Ponente")]/following-sibling::text()[1]
# Magistrado AV=./td/p[1]/strong[contains(text(),"Magistrado Ponente")]/following-sibling::text()[1]
# Magistrado Ponente=./td/p[1]/strong[contains(text(),"Magistrado Ponente")]/following-sibling::text()[1]
# Magistrado Aclaracion Voto=./td/p[1]/strong[starts-with(.,"AV")]/following-sibling::text()[1]
# Magistrado Aclaracion PArcial Voto=./td/p[1]/strong[starts-with(.,"APV")]/following-sibling::text()[1]
# Magistrado Salvamento Voto=./td/p[1]/strong[starts-with(.,"SV") or starts-with(.,"PV") or starts-with(.,"SOV")]/following-sibling::text()[1]
# Magistrado Salvamento Parcial Voto=./td/p[1]/strong[starts-with(.,"SPV")]/following-sibling::text()[1]
# Demandate VS Demandado=./td/p[1]/strong[starts-with(.,"Demandante")]/following-sibling::text()[1]
# Tema=./td/p[2]/strong[text()="Tema:"]/following-sibling::text()[1]
# Recibo Relatoria=./td/p[2]/strong[contains(text(),"Recibo Relatoria")]/following-sibling::text()[1]
# Pagina siguiente=//*[@class="pagination"]//a[text()="Siguiente »"]


class CorteConstitucionalSpider(scrapy.Spider):
    page: int = 0

    name = 'corteconstitucional'
    allowed_domains = ['www.corteconstitucional.gov.co']
    custom_settings = {
        'CONCURRENT_REQUESTS': 24,
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        anios_init = int(getattr(self, 'anios_init', 19))
        anios_limit = int(getattr(self, 'anios_limit', 19))
        for anios in range(anios_init, anios_limit+1):
            yield scrapy.Request(f'https://www.corteconstitucional.gov.co/relatoria/radicador/buscar.php?anios={anios}&pg={self.page}')

    def parse(self, response):
        for sentence_item in response.xpath('//tr[contains(@onmouseover, "uno(this")]'):
            try:
                item = StripFirstItemLoader(JuriscolItem(), sentence_item)
                # First paragraph
                item.add_xpath(
                    "file_id", './td/p[1]/strong[contains(.,"Expediente")]/following-sibling::text()[1]')
                item.add_xpath(
                    "date", './td/p[1]/strong[contains(.,"Fecha sentencia")]/following-sibling::text()[1]')
                item.add_xpath(
                    "sentence_id", './td/p[1]/strong[contains(.,"Sentencia")]/following-sibling::a/text()')
                item.add_xpath(
                    "magistrate", './td/p[1]/strong[contains(.,"Magistrado Ponente")]/following-sibling::text()[1]')
                item.add_xpath(
                    "magistrate_av", './td/p[1]/strong[starts-with(.,"AV")]/following-sibling::text()[1]')
                item.add_xpath(
                    "magistrate_apv", './td/p[1]/strong[starts-with(.,"APV")]/following-sibling::text()[1]')
                item.add_xpath(
                    "magistrate_sv", './td/p[1]/strong[starts-with(.,"SV") or starts-with(.,"PV") or starts-with(.,"SOV")]/following-sibling::text()[1]')
                item.add_xpath(
                    "magistrate_spv", './td/p[1]/strong[starts-with(.,"SPV")]/following-sibling::text()[1]')

                pair = sentence_item.xpath(
                    './td/p[1]/strong[starts-with(.,"Demandante")]/following-sibling::text()[1]').get().split("VS")
                item.add_value("plaintiff", pair[0])
                item.add_value("defendant", pair[1] if len(pair) > 1 else None)

                item.add_xpath(
                    "topic", './td/p[2]/strong[text()="Tema:"]/following-sibling::text()[1]')
                item.add_xpath(
                    "report_receipt_at", './td/p[2]/strong[contains(text(),"Recibo Relatoria")]/following-sibling::text()[1]')

                # sentence's text
                yield response.follow(
                    sentence_item.xpath(
                        './td/p[1]/strong[contains(.,"Sentencia")]/following-sibling::a/@href').get(),
                    callback=self.parse_text, cb_kwargs={'item': item})
            except Exception:
                raise

        next_page = response.xpath(
            '//*[@class="pagination"]//a[text()="Siguiente »"]').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_text(self, response, item, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        txt = soup.div.get_text()
        item.add_value('text', txt)
        item.add_value('url', response.url)
        item.add_value('source', self.name)
        yield item.load_item()
