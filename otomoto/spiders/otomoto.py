from parso import parse
import scrapy
import re

from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Compose

from otomoto.items import OtomotoItem


def filter_out_array(x):
    x = x.strip()
    return None if x == "" else x


def remove_spaces(x):
    return x.replace(" ", "")


def convert_to_integer(x):
    return int(x)


class OtomotoCarLoader(ItemLoader):
    default_output_processor = TakeFirst()

    features_out = MapCompose(filter_out_array)
    price_out = Compose(TakeFirst(), remove_spaces, convert_to_integer)


class OtomotoSpider(scrapy.Spider):

    allowed_domains = ("otomoto.pl",)
    name = "otomoto"
    page_number = 0
    start_urls = ["https://www.otomoto.pl"]

    def __init__(self, brand, max_sites):
        self.brand = brand
        self.max_sites = int(max_sites)

    # def parse(self, response):
    #     for brand, max_sites in self.car_brands.items():
    #         base_page = f"https://www.otomoto.pl/osobowe/{brand}/page=0"
    #         self.current_brand = brand
    #         self.max_sites = max_sites
    #         yield response.follow(base_page, self.parse_brand, dont_filter=True)

    def parse(self, response):
        print(f"BRAND: {self.brand} PAGE_NUMBER: {self.page_number}")
        try:
            raw_data = response.xpath(
                "/html/body/div[1]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[3]/main"
            ).extract()[0]

            links = re.findall("href=[\"'](.*?)[\"']", raw_data)
            final_links = [link for link in links if "oferta" in link]

            for car_page in final_links:
                yield response.follow(car_page, self.parse_car_page, dont_filter=True)


        except IndexError:
            print(f"INDEX ERROR ERROR_COUNT")

        next_page = f"https://www.otomoto.pl/osobowe/{self.brand}/page={self.page_number}"
        print(response.request.url)
        if self.page_number <= self.max_sites:
            OtomotoSpider.page_number += 1  
            yield response.follow(next_page, self.parse, dont_filter=True)

    def parse_car_page(self, response):
        property_list_map = {
            "Marka pojazdu": "brand",
            "Model pojazdu": "model",
            "Rok produkcji": "year",
            "Wersja": "version",
            "Przebieg": "mileage",
            "Pojemność skokowa": "capacity",
            "Moc": "horse_power",
            "Rodzaj paliwa": "fuel_type",
            "Skrzynia biegów": "transmission",
            "Typ": "type",
            "Liczba drzwi": "number_of_doors",
            "Kraj pochodzenia": "origin_country",
            "Kolor": "color",
            "Pierwszy właściciel": "first_owner",
            "Bezwypadkowy": "no_accidents",
            "Serwisowany w ASO": "aso",
            "Stan": "condition",
        }
        loader = OtomotoCarLoader(OtomotoItem(), response=response)

        for params in response.css(".offer-params__item"):
            property_name = (
                params.css(".offer-params__label::text").extract_first().strip()
            )
            if property_name in property_list_map:
                css = params.css(".offer-params__value::text").extract_first().strip()
                if css == "":
                    css = params.css("a::text").extract_first().strip()
                loader.add_value(property_list_map[property_name], css)

        loader.add_css("price", ".offer-price__number::text")
        loader.add_css("price_currency", ".offer-price__currency::text")

        loader.add_css("features", ".offer-features__item::text")
        loader.add_value("url", response.url)

        yield loader.load_item()
