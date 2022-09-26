import scrapy, re
from ep1.items import Pokemon, DamageByType


class Scraper(scrapy.Spider):
    name = "poke-scraper"
    start_urls = ['https://pokemondb.net/pokedex/game/red-blue-yellow']

    def parse(self, response):
        urls = response.css('#main > div.infocard-list.infocard-list-pkmn-lg > div > span.infocard-lg-img > a::attr(href)')

        for url in urls:
            yield response.follow(url.get(), self.parse_pokemon)

    def parse_pokemon(self, response):
        damagesbytype = []
        tab = response.css('#main > div.tabset-basics.sv-tabs-wrapper.sv-tabs-onetab > div.sv-tabs-tab-list > a::attr(href)').get() or re.search('#tab-basic-(\d+)', response.body.decode("utf-8")).group(0)

        types = response.css(f'{tab} > div:nth-child(2) > div.grid-col.span-md-12.span-lg-4 > div > table > tr > th > a::attr(title)').getall()

        if not types:
            alternative_tab = re.search('#tab-typedefcol-(.+?)"', response.body.decode("utf-8")).group(0).replace('"', "")
            types = response.css(f'{alternative_tab} > div > table > tr > th > a::attr(title)').getall()

        damages = response.css(f'{tab} > div:nth-child(2) > div.grid-col.span-md-12.span-lg-4 > div > table > tr > td').xpath("normalize-space()").getall()

        if not damages:
            alternative_tab = re.search('#tab-typedefcol-(.+?)"', response.body.decode("utf-8")).group(0).replace('"', "")
            damages = response.css(f'{alternative_tab} > div > table > tr > td').xpath("normalize-space()").getall()

        for i, v in enumerate(types):
            damagesbytype.append(DamageByType(damages[i], types[i]))

        pokemon = Pokemon(
            number=response.css(f'{tab} > div:nth-child(1) > div:nth-child(2) > table > tbody > tr:nth-child(1) > td > strong::text').get(),
            name=response.css('#main > h1::text').get(),
            _evolutions=response.css('#main > div.infocard-list-evo > div > span.infocard-lg-data.text-muted > a::text').getall(),
            height=response.css(f'{tab} > div:nth-child(1) > div:nth-child(2) > table > tbody > tr:nth-child(4) > td::text').get(),
            weight=response.css(f'{tab} > div:nth-child(1) > div:nth-child(2) > table > tbody > tr:nth-child(5) > td::text').get(),
            _types=response.css(f'{tab} > div:nth-child(1) > div:nth-child(2) > table > tbody > tr > td > a::text').getall(),
            _damage_taken_by_type=damagesbytype
        )

        yield pokemon