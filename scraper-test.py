import requests
from bs4 import BeautifulSoup
import cloudscraper
import csv
import re

output_file = "notino_transformed.csv"
output_data = []

print("Processing...")


def scrape_page(url):
    """
    Scrapes url on notino.cz website and returns product name, brand , price, url and image
    """
    scraper = cloudscraper.create_scraper()
    content_url = scraper.get(url).text
    soup = BeautifulSoup(content_url, "html.parser")
    return soup

output_dict = {}

for i in range(1, 25):
    url = f"https://www.notino.cz/zubni-pasty/?f={i}-1-2-4891-7183"
    page_data = scrape_page(url)

    products = page_data.select("h3.sc-dmyCSP")
    brands = page_data.select("h2.sc-guDLey")
    prices = page_data.select("span.sc-hhyKGa.sc-gYrqIg.iwwcvf.dOVzXZ")
    links = page_data.select(".sc-jdHILj")
    images = page_data.select(".sc-iKOmoZ.gTqEqC")

    for product, brand, price, link, image in zip(products, brands, prices, links, images):
        product_out = product.text.strip()
        brand_out = brand.text.strip()
        price_out = price.text.strip()
        link_out = f"https://www.notino.cz{(link.get('href'))}".strip()
        image_out = image.get('src').strip()

        output_dict = {
            "Product Name": product_out,
            "Brand": brand_out,
            "Price": price_out,
            "Link": link_out,
            "Image": image_out
        }

        output_data.append(output_dict)

with open(output_file, "w", newline="", encoding="utf-8") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=output_dict.keys())
    writer.writeheader()
    for product in output_data:
        writer.writerow(product)

print("Successfully printed.")
