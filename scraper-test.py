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

#test
output_dict = {}

for i in range(1, 25):
    url = f"https://www.notino.cz/zubni-pasty/?f={i}-1-2-4891-7183"
    page_data = scrape_page(url)

    products = page_data.select("h3.sc-dmyCSP")
    brands = page_data.select("h2.sc-guDLey")
    # # prices = page_data.select("span.sc-hhyKGa")
    # # prices = page_data.find("span", {"class": "sc-hhyKGa sc-gYrqIg iwwcvf dOVzXZ"})

    # # for product in products:
    # #     product_out = product.text.strip()
    # #     output_dict["Brand"] = product_out

    for product, brand in zip(products, brands):
        product_out = product.text.strip()
        brand_out = brand.text.strip()
        # price_out = price.text.strip()

        output_dict = {
            "Product Name": product_out,
            "Brand": brand_out,
            # "Price": price_out,
        }
    #     output_data.append(output_dict)
    # for price in page_data:
    #     price = page_data.find("span", {"class": "sc-hhyKGa sc-gYrqIg iwwcvf dOVzXZ"})
    #     output_dict["Price"] = price
    # links = page_data.select(".sc-jdHILj")

    # for link in links:

    #     output_dict["Url"] = f"https://www.notino.cz{(link.get('href'))}".strip()
 
        output_data.append(output_dict)

with open(output_file, "w", newline="", encoding="utf-8") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=output_dict.keys())
    writer.writeheader()
    for product in output_data:
        writer.writerow(product)

print("Successfully printed.")
