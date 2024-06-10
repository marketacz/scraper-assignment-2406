# Scraper Assignment
1) `notino/scraper.py` - Scrapes data from Notino website about toothpastes (https://www.notino.cz/zubni-pasty/) and transform them.
 * Gets info about products: product name, brand, price, url, image
 * Saves result to csv file `notino_raw.csv`
3) `notino/transformation.py` - Transformation of raw data to final format
 * Adds country (str), currency (str) and scraped_at (datetime) columns
 * Adds discount amount column (difference between price and price before sale or promocode)
 * Saves result to csv file `notino_transformed.csv`
