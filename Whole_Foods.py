# Description: This script is the main file, run the script in your terminal to interact with the GUI & see the output

# import pandas as pd
import requests 

import time
# import urllib
from bs4 import BeautifulSoup

#import a bunch fo stuff from selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chromedriver_autoinstaller

# Beautiful Soup scraping for Whole Foods website
def scrape_whole_foods(search_keyword, zip_code_placeholder, product_number_userinput):
    #initialize lists
    brand_list = []
    product_name_list = []
    price_list = []
    img_url_list = []
    url_list = []

    # Set up Chrome options for headless browsing, no more pop up windows! annoying!
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #!!!!!!!!!!! if you want to use a different path for downloaded WEBDRIVER, change it here !!!!!!!!!!!!!!
    # PATH = "Users/yibofu/Downloads/chromedriver-mac-arm64/chromedriver"

    #antoher way to set up chrome driver without version problem
    chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path
    driver = webdriver.Chrome(options=chrome_options)
    
    #modify the url with the search keyword
    driver.get('https://www.wholefoodsmarket.com/search?text={:<}'.format(search_keyword))
    # wait for the 'box' element to appear, no more than 5s
    wait = WebDriverWait(driver, 2)
    element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wfm-search-bar--input")))
    # print(element) #really weird fetched result (not a html tag), but it works

    #now the element should appeared, type the zip code and hit Enter!
    #text_area = driver.find_element_by_class_name('wfm-search-bar--input')
    text_area = driver.find_element(By.CLASS_NAME, 'wfm-search-bar--input')
    # print(zip_code)
    text_area.send_keys(zip_code_placeholder)
    text_area.send_keys(Keys.RETURN)

    #wait again for the zip code to be processed
    selection = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.wfm-search-bar--list_item")))

    #now click the first item(store name) in the list
    driver.execute_script("arguments[0].click();", selection)
    #wait for a while for the page with price to load
    time.sleep(1)

    #finally! fetch the loaded page elements using beautiful soup
    soup = BeautifulSoup(driver.page_source, 'html.parser') # Hey if this line causes an error, run 'pip install html5lib' or install html5lib 
    div_box = soup.find_all("div", class_="w-pie--product-tile__content")
    # print(div_box) 
    #find out brand, name, price
    for element in div_box[:product_number_userinput]:
        product_brand = element.find("span", class_="w-cms--font-disclaimer")
        brand_list.append(product_brand.text)
 
        product_name = element.find("h2", class_="w-cms--font-body__sans-bold")
        product_name_list.append(product_name.text)

        product_price = element.find("span", class_="text-left bds--heading-5")
        if product_price:
            price_list.append(product_price.text)
        else:
            price_list.append("Price not available")

    #print(brand_list)
    #print(product_name_list)
    #print(price_list)

    imgResults = driver.find_elements(By.XPATH,"//img[contains(@class,'ls-is-cached lazyloaded')]")
    for img in imgResults[:product_number_userinput]:
        img_url_list.append(img.get_attribute('src'))
    #print(img_url_list)

    #get url to each product page
    url_box = soup.find_all('a', class_='w-pie--product-tile__link')
    for each_url_box in url_box[:product_number_userinput]:
        url = 'wholefoodsmarket.com' + each_url_box.get('href')  # Extract the href attribute
        url_list.append(url)
    #print(url_list)
    #i dont understand why this donest work, so i have to use beautiful soup to get the url -^-
    # url_div = driver.find_elements_by_class_name('w-pie--product-tile__link')
    # print(url_div)
    # for url in url_div:
    #     url_list.append(url.get_attribute('href'))
    # print(url)

    #regular expression to extract the unit
    import re
    #real product name list deducted from ','
    product_name_cleaned_list = [re.sub(r',.*', '', each_element) for each_element in product_name_list]
    #put the rest into unit list and flatten it
    unit_list = [re.findall(r'\d.*', each_element) for each_element in product_name_list]
    unit_flattened_list = [element[0] if element else 'N/A' for element in unit_list]

    #print(product_name_cleaned_list)
    #print(unit_flattened_list)
    print(img)
    driver.quit()

    return brand_list, product_name_cleaned_list, price_list, unit_flattened_list, url_list, img_url_list

    #this will be a seperate functions: panda datafrme
    #ls = [brand_list, product_name_cleaned_list,  price_list, unit_flattened_list, img_url_list, url_list]
    #df = pd.DataFrame(ls).transpose()
    #df.columns = ['Brand', 'Product Name', 'Price', 'Unit', 'Image URL', 'Product URL']
    #print(df)
    
    

if __name__ == '__main__':
    print('this is the script scrapping from whole foods')
    scrape_whole_foods('Milk', 15222, 1)