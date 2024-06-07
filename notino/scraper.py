import requests
from bs4 import BeautifulSoup
import cloudscraper
import csv
import re

output_file = "notino_raw.csv"
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

for i in range(1, 25):
    # Construct URL for each page of toothpaste products on notino.cz
    url = f"https://www.notino.cz/zubni-pasty/?f={i}-1-2-4891-7183"
    # Call the scrape_page function to get page data
    page_data = scrape_page(url)

    # Select elements containing product names, brands, prices, links, and images
    products = page_data.select("h3.sc-dmyCSP")
    brands = page_data.select("h2.sc-guDLey")
    prices = page_data.select('span[data-testid="price-component"]')
    links = page_data.select(".sc-jdHILj")
    images = page_data.select(".sc-iKOmoZ.gTqEqC")

    # Iterate through each product element and extract relevant information
    for idx, (product, brand, price, link, image) in enumerate(zip(products, brands, prices, links, images)):
        product_out = product.text.strip()
        brand_out = brand.text.strip()
        price_out = float(price.text.strip().replace('\xa0', '').replace(',','.'))

        # Select discount for each product by index
        discount_elements = page_data.select(".styled__DiscountValue-sc-1b3ggfp-1.jWXmOz")
        discount_out = "0"
        if idx < len(discount_elements):
            discount_out = float(discount_elements[idx].text.strip().replace(' %',''))
        
        link_out = f"https://www.notino.cz{link['href']}".strip()
        image_out = image['src'].strip()

        # Create a dictionary containing the extracted information for each product
        output_dict = {
            "Product Name": product_out,
            "Brand": brand_out,
            "Price": price_out,
            "Discount": discount_out,
            "Link": link_out,
            "Image": image_out
        }

        # Append the dictionary to the output_data list if it's not already present
        if output_dict not in output_data:
            output_data.append(output_dict)

# Write the collected data to a CSV file
with open(output_file, "w", newline="", encoding="utf-8") as file_out:
    writer = csv.DictWriter(file_out, fieldnames=output_dict.keys())
    writer.writeheader()
    for product in output_data:
        writer.writerow(product)

print("Successfully printed.")
