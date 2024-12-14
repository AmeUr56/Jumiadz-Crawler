
# Jumiadz Crawler

This is a simple Scrapy-based web crawler designed to scrape cproducts from the Jumia dz website and store them in a csv file.

## Features
- Scrapes product details such as id, category, name, url, brand, price, rating and number of ratings.
- Stores scraped data in an csv file.

## Installation

#### 1. Clone the repository:
```
git clone https://github.com/AmeUr56/Jumiadz-Crawler
```
#### 2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Running the Crawler

#### 1. Run the Scrapy spider:
```
scrapy crawl <spider-name>
```
#### 2. The data will be inserted into an CSV file.

## CSV File
The csv table includes the following columns:
- `product_id`
- `category`
- `name`
- `url`
- `brand`
- `price`
- `rating`
- `rating_count`

## License
This project is licensed under the MIT License.
