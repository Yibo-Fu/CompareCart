import time
from selenium import webdriver
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import Entry, Label, Button, scrolledtext
#antoher way to set up chrome driver without version problem
import chromedriver_autoinstaller

def scrape_data(search_keyword):
    # Define the base URL and URL parts
    base_url = 'https://new.aldi.us/results?q='
    url_pt1 = ''
    url_pt2 = ''

    # Combine the base URL, search keyword, and URL parts
    target_url = f'{base_url}{search_keyword}'
    # Set up a headless browser (make sure you have the appropriate webdriver installed)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')       
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
    driver = webdriver.Chrome(options=options)


    # Load the page
    driver.get(target_url)

    # Allow some time for the page to load dynamically (adjust sleep time as needed)
    time.sleep(5)

    # Get the page source after it has loaded dynamically
    page_source = driver.page_source

    # Close the headless browser
    driver.quit()
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup

 

def scrape_product_grid_details(soup):
    # Find the div tag with the specified class
    product_grid_div = soup.find('div', class_='product-grid')

    # Create a list to store product details
    product_details = []

    # Check if the product grid div is found
    if product_grid_div:
        # Find all nested divs within the product grid div
        nested_divs = product_grid_div.find_all('div', id=True)  # Find all divs with id attribute

        # Iterate through all nested divs
        for nested_div in nested_divs:
            # Extract the id attribute and other details as needed
            product_id = nested_div['id']
           

            # Append the product details to the list
            product_details.append({'product_id': product_id})


    return product_details

def scrape_img_src_from_specific_div(soup, div_id):
    # Find the div with the specified ID
    specific_div = soup.find('div', id=div_id)

    # Check if the specific div is found
    if specific_div:
        # Find the img tag within the specific div
        img_tag = specific_div.find('img', src=True)

        # Check if an img tag is found
        if img_tag:
            # Extract the src attribute
            img_src = img_tag['src']


            return img_src

    # Return None if the specific div or img src is not found
    return None

def scrape_brandname_from_specific_div(soup, div_id):
    # Find the div with the specified ID
    specific_div = soup.find('div', id=div_id)

    # Check if the specific div is found
    if specific_div:
        # Find the nested div with the class "product-tile__brandname"
        brandname_div = specific_div.find('div', class_='product-tile__brandname')

        # Check if the brandname div is found
        if brandname_div:
            # Extract the text content of the brandname div
            brandname = brandname_div.get_text(strip=True)

            return brandname

    # Return None if the specific div or brandname is not found
    return None


def scrape_product_name_from_specific_div(soup, div_id):
    # Find the div with the specified ID
    specific_div = soup.find('div', id=div_id)

    # Check if the specific div is found
    if specific_div:
        # Find the nested div with the class "product-tile__name"
        product_name_div = specific_div.find('div', class_='product-tile__name')

        # Check if the product name div is found
        if product_name_div:
            # Extract the text content of the product name div
            product_name = product_name_div.get_text(strip=True)

            return product_name

    # Return None if the specific div or product name is not found
    return None
def scrape_unit_quantity_from_specific_div(soup, div_id):
    # Find the div with the specified ID
    specific_div = soup.find('div', id=div_id)

    # Check if the specific div is found
    if specific_div:
        # Find the nested div with the class "product-tile__unit-of-measurement"
        unit_quantity_div = specific_div.find('div', class_='product-tile__unit-of-measurement')

        # Check if the unit quantity div is found
        if unit_quantity_div:
            # Extract the text content of the unit quantity div
            unit_quantity = unit_quantity_div.get_text(strip=True)

            return unit_quantity

    # Return None if the specific div or unit quantity is not found
    return None

def scrape_price_from_specific_div(soup, div_id):
    # Find the div with the specified ID
    specific_div = soup.find('div', id=div_id)

    # Check if the specific div is found
    if specific_div:
        # Find the nested div with the class "base-price product-tile__price base-price--product-tile"
        price_div = specific_div.find('div', class_='base-price product-tile__price base-price--product-tile')

        # Check if the price div is found
        if price_div:
            # Extract the text content of the price div
            price = price_div.get_text(strip=True)

            return price

    # Return None if the specific div or price is not found
    return None


def search_button_clicked(search_keyword, num_of_products):
    num_of_products = num_of_products
    all_product_details = []

    # Call the scrape_data function with the search keyword
    soup = scrape_data(search_keyword)

    product_list_details = scrape_product_grid_details(soup)

    for product_details in product_list_details[:num_of_products]:
        product_id = product_details['product_id']
        image_src = scrape_img_src_from_specific_div(soup, product_id)
        brand_name = scrape_brandname_from_specific_div(soup, product_id)
        product_title = scrape_product_name_from_specific_div(soup, product_id)
        product_quantity = scrape_unit_quantity_from_specific_div(soup, product_id)
        product_price = scrape_price_from_specific_div(soup, product_id)

        # URL formation for the product
        brand_name_lower = brand_name.lower()
        extracted_product_name = product_title.split(',')[0].strip()
        extracted_product_name_lower = extracted_product_name.lower().replace(" ", "-")
        extracted_product_id = product_id.split('-')[2].strip()
        product_URL = f'https://new.aldi.us/product/{brand_name_lower}-{extracted_product_name_lower}-{extracted_product_id}'
        product_URL = product_URL.replace('%', '')
        product_URL = product_URL.replace(' ', '-')

        all_product_details.append({
            'product_URL': product_URL,
            'product_name': product_title,
            'product_brand': brand_name,
            'product_price': product_price,
            'image_src': image_src
        })

    print(all_product_details)
    return all_product_details

