import scrapy
from juriscol.items import StripFirstItemLoader, JuriscolItem
from nlp_pos.transform import SpacyDoc


class CorteConstitucionalSpider(scrapy.Spider):
    page: int = 0
    # anios = getattr(self, 'anios', 2019)
    name = 'corteconstitucional'
    allowed_domains = ['www.corteconstitucional.gov.co']
    # start_urls = [
    #     f'https://www.corteconstitucional.gov.co/relatoria/radicador/buscar.php?anios={anios}&pg={page}']

    def start_requests(self):
        for anios in range(16, 20):
            yield scrapy.Request(f'https://www.corteconstitucional.gov.co/relatoria/radicador/buscar.php?anios={anios}&pg={self.page}')

    def parse(self, response):
        for sentencia_item in response.xpath('//tr[contains(@onmouseover, "uno(this")]'):
            try:

                if not len(sentencia_item.xpath('./td/p[1]//text()[2]').get().strip()):
                    continue

                item = StripFirstItemLoader(JuriscolItem(), sentencia_item)
                item.add_xpath("expediente", "./td/p[1]/text()[2]")
                item.add_xpath(
                    "fecha_sentencia", './td/p[1]/strong[contains(text(),"Fecha sentencia")]/following-sibling::text()[1]')
                item.add_xpath("sentencia_id", "./td/p[1]//a/text()[1]")

                item.add_xpath(
                    "magistrado", './td/p[1]/strong[contains(text(),"Magistrado Ponente")]/following-sibling::text()[1]')

                pair = sentencia_item.xpath(
                    './td/p[1]/strong[contains(text(),"Demandante")]/following-sibling::text()[1]').get().split("VS.")
                item.add_value("demandante", pair[0])
                item.add_value("demandado", pair[1] if len(pair) > 1 else None)

                item.add_xpath(
                    "tema", './td/p[2]/strong[text()="Tema:"]/following-sibling::text()[1]')
                item.add_xpath(
                    "recibo_relatoria", './td/p[2]/strong[contains(text(),"Recibo Relatoria")]/following-sibling::text()[1]')

                yield response.follow(
                    sentencia_item.css('a::attr(href)').get(),
                    callback=self.parse_sentencia,
                    cb_kwargs={'item': item})
            except:
                print("DDDD-----------------")
                print(sentencia_item.xpath("./td/p[1]/text()[2]").extract())
                print(sentencia_item.xpath(
                    './td/p[1]/strong[contains(text(),"Demandante")]/following-sibling::text()[1]').get().split("VS."))
                raise

        next_page = response.xpath(
            '//*[@class="pagination"]//a[text()="Siguiente »"]').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_sentencia(self, response, item):
        item.add_value('url', response.url)
        txt = "".join(response.xpath(
            '//div[@class="WordSection1"]//text()').extract())
        item.add_value('texto_sentencia', txt)
        doc = SpacyDoc(txt)
        item.add_value('entidades', doc.entities)
        item.add_value('palabras', doc.pos)
        return item.load_item()
