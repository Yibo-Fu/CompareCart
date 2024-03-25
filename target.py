import requests
import csv
import pandas as pd
from io import StringIO
import re
import time

def scrape_data(search_keyword, num_of_products, max_retries=7, delay=3):
    # set up the request parameters
    params = {
        'api_key': '6219C472B164473B934E388959DE3052',
        'search_term': search_keyword,
        'type': 'search',
        'output': 'csv',
        'csv_fields': 'search_results.product.title,search_results.product.link,search_results.product.main_image,search_results.product.brand,search_results.offers.primary.price,search_results.offers.primary.regular_price'
    }

    retries = 0
    while retries < max_retries:
        try:
            # HTTP GET Request by using RedCircle API
            api_result = requests.get('https://api.redcircleapi.com/request', params)

            # Check for successful response
            if api_result.status_code == 200:
                csv_data = StringIO(api_result.content.decode('utf-8'))
                reader = csv.DictReader(csv_data)

                scraped_data = [row for row in reader]
                # print(scraped_data)
                if scraped_data:
                    return scraped_data[:num_of_products]  # Return data if scraping is successful
            else:
                raise Exception(f"Bad response: {api_result.status_code}")

        except Exception as e:
            print(f"Error occurred: {e}. Retrying in {delay} seconds.")
            time.sleep(delay)  # Wait before retrying
            retries += 1

    print("Max retries reached. Exiting.")
    return None

if __name__ == '__main__':
    # Get the search keyword from the user
    search_keyword = input("Enter search keyword: ")

    # Call the scrape_data function with the search keyword
    scraped_data = scrape_data(search_keyword)

