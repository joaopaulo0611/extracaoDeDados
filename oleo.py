import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import scrapy


class OleoSpider(scrapy.Spider):
    name = "oleo"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'LOG_FILE': 'scrapy_output.log',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_EXPIRATION_SECS': 86400,
        'HTTPCACHE_DIR': 'cache',
        'HTTPCACHE_IGNORE_HTTP_CODES': [404, 500, 502, 503]
    }

    start_urls = [
        "https://www.giassi.com.br/sitemap/product-0.xml",
        "https://www.giassi.com.br/sitemap/product-1.xml",
        "https://www.giassi.com.br/sitemap/product-2.xml",
        "https://www.giassi.com.br/sitemap/product-3.xml",
        "https://www.giassi.com.br/sitemap/product-4.xml",
        "https://www.giassi.com.br/sitemap/product-5.xml",
        "https://www.giassi.com.br/sitemap/product-6.xml",
        "https://www.giassi.com.br/sitemap/product-7.xml",
        "https://www.giassi.com.br/sitemap/product-8.xml",
        "https://www.giassi.com.br/sitemap/product-9.xml",
        "https://www.giassi.com.br/sitemap/product-10.xml",
        "https://www.giassi.com.br/sitemap/product-11.xml",
        "https://www.giassi.com.br/sitemap/product-12.xml",
    ]

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.set("BOT_NAME", "Pesquisa_Oleo_Giassi", priority="spider")
        settings.set("ITEM_PIPELINES", {"pipelines.SQLAlchemyPipeline": 300}, priority="spider")

    def parse(self, response: scrapy.http.Response):
        response.selector.remove_namespaces()
        # buscar ulr que comaça com óleo e contem 900ml
        produtos_oleo = response.xpath('//url/loc[contains(text(),".com.br/oleo_") and contains(text(),"900ml")]/text()').getall()
        print(f'Encontrados {len(produtos_oleo)} produtos de óleo 900ml neste sitemap')

        for url in produtos_oleo:
            yield response.follow(url, self.parse_produto)

    def parse_produto(self, response: scrapy.http.Response):
        # extrai nome do produto
        url_path = response.url.split('/')[-2]
        nome_formatado = url_path.rsplit('_', 1)[0].replace('_', ' ').title()
        preco = response.xpath('//script[@type="application/ld+json"]/text()').re_first(r'"price":\s*"?(\d+\.?\d*)"?')

        if not preco:
            preco = response.xpath('//meta[@property="product:price:amount"]/@content').get()

        if not preco:
            preco = "Preço não disponível"

        yield {
            'produto': nome_formatado,
            'preco': preco,
            'url': response.url
        }
