from scrapy.crawler import CrawlerProcess
import os
from time import sleep

process = CrawlerProcess(
    settings={
        "FEEDS": {
            "data.csv": {"format": "csv"},
        },
    }
)

car_brands = {
    "rolls-royce": 1,
    "mini": 40,
    "audi": 425,
    "opel": 422,
    "bmw": 416,
    "volkswagen": 408,
    "ford": 369,
    "mercedes-benz": 293,
    "renault": 270,
    "toyota": 216,
    "skoda": 212,
    "alfa-romeo": 41,
    "Bentley": 3,
    "chevrolet": 46,
    "citroen": 180,
    "dacia": 60,
    "dodge": 24,
    "ferrari": 2,
    "fiat": 132,
    "honda": 98,
    "hyundai": 168,
    "jaguar": 29,
    "jeep": 49,
    "kia": 156,
    "lamborghini": 1,
    "land-rover": 34,
    "lexus": 28,
    "maserati": 7,
    "mclaren": 1,
    "mazda": 111,
    "mitsubishi": 54,
    "nissan": 136,
    "peugeot": 206,
    "porsche": 32,
    "saab": 11,
    "suzuki": 67,
    "seat": 116,
    "volvo": 143,
}


def scrape_otomoto(brand_dict):
    for brand, max_sites in brand_dict.items():
        print(f"STARTING {brand} SCRAPER")
        os.system(
            f"scrapy crawl -L WARNING otomoto -a brand={brand} -a max_sites={max_sites} -o df.csv"
        )
        sleep(5)


if __name__ == "__main__":
    scrape_otomoto(car_brands)
