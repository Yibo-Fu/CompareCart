import sys
from PyQt5.QtWidgets import QApplication
from input_screen import InputScreen  # Import the modified InputScreen class
from output_screen import create_output_window  # Import the function from output_screen.py
# Three scraping files
import ALDI_scraping
from Whole_Foods import scrape_whole_foods
from target import scrape_data
import re



if __name__ == '__main__':
        # Initialize variables
    scraped_data = None
    scraped_data_target = None
    whole_foods_data = None

    app = QApplication(sys.argv)

    # Create and display the input screen
    input_screen = InputScreen()
    input_screen.show()

    # Wait for the input screen to finish
    app.exec_()

    # Retrieve the input values
    product_name, num_of_products, zip_code = input_screen.get_values()
    num_of_products = int(num_of_products)

    # Call ALDI_scraping.py
    scraped_data = ALDI_scraping.search_button_clicked(product_name, num_of_products)
    # Call target.py scrape_data
    scraped_data_target = scrape_data(product_name, num_of_products)
    # Call scrape_whole_foods function
    whole_foods_data = scrape_whole_foods(product_name, zip_code, num_of_products)
    



# ALDI
aldi_products = []
if scraped_data:
    for product in scraped_data:
        product_brand_aldi = product.get('product_brand', '')
        product_name_aldi = product.get('product_name', '')
        product_price_aldi = product.get('product_price', '')
        unit_price_aldi = "N/A"
        unit_infor_aldi = "N/A"
        product_url_aldi = product.get('product_URL', '')
        product_img_url_aldi = product.get('image_src', '')

        aldi_products.append({
            'product_brand': product_brand_aldi,
            'product_name': product_name_aldi,
            'product_price': product_price_aldi,
            'unit_price': unit_price_aldi,
            'unit_infor': unit_infor_aldi,
            'product_url': product_url_aldi,
            'product_img_url': product_img_url_aldi,
            'logo_path': 'ALDI.jpg'
        })
else:
    aldi_products = []

#Target
target_products = []

if scraped_data_target:
    for product in scraped_data_target:
        product_name_target = product['search_results.product.title']
        brand_target = product['search_results.product.brand']
        price_target = product['search_results.offers.primary.price']
        unit_price_target = "N/A"
        unit_infor_target = "N/A"
        product_url_target = product['search_results.product.link']
        product_img_url_target = product['search_results.product.main_image']

        product_brand_target = brand_target
        product_name_target = product_name_target
        product_name_target = re.sub(r'&.*?;', '', product_name_target)

        target_products.append({
            'product_brand': brand_target,
            'product_name': product_name_target,
            'product_price': price_target,
            'unit_price': unit_price_target,
            'unit_infor': unit_infor_target,
            'product_url': product_url_target,
            'product_img_url': product_img_url_target,
            'logo_path': 'TG.jpg'
        })
else:
    target_products = []


#wholeFoods
whole_foods_products = []
if whole_foods_data:
    print(len(whole_foods_data))
    for i in range(len(whole_foods_data[1])):
        brand_name_whole = whole_foods_data[0][i] if whole_foods_data[0] else ""
        product_name_whole = whole_foods_data[1][i] if whole_foods_data[1] else ""
        price_whole = whole_foods_data[2][i] if whole_foods_data[2] else ""
        unit_infor_whole = whole_foods_data[3][i] if whole_foods_data[3] else ""
        product_url_whole = whole_foods_data[4][i] if whole_foods_data[4] else ""
        product_img_url_whole = whole_foods_data[5][i] if whole_foods_data[5] else ""
        unit_price_whole = "N/A"

        product_name_whole = product_name_whole
        product_brand_whole = brand_name_whole

        whole_foods_products.append({
            'product_brand': product_brand_whole,
            'product_name': product_name_whole,
            'product_price': price_whole,
            'unit_price': unit_price_whole,
            'unit_infor': unit_infor_whole,
            'product_url': product_url_whole,
            'product_img_url': product_img_url_whole,
            'logo_path': 'WF.jpg'
        })
else:
    whole_foods_products = []


all_products = aldi_products + target_products + whole_foods_products
# output_screen.create_output_window(product_name, all_products)# Display the output screen

# Call the function to create and display the output window
create_output_window(product_name, all_products)



