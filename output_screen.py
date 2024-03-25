from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from io import BytesIO
import webbrowser

# Function to open a web URL in the default browser
def open_url(url):
    webbrowser.open(url, new=2)  # new=2 specifies that a new tab should be opened, if possible

# Function that reads web-picture
def load_web_image(url, default_image='NF.jpg', size=(120, 120)):
    try:
        response = requests.get(url)
        image = QPixmap()
        image.loadFromData(response.content)
    except Exception as e:
        print(f"Error loading web image: {e}, using default image.")
        image = QPixmap(default_image)

    image = image.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return image

# Function that re-sizes and displays each company logo picture
def load_image(file_path, size=(120, 120)):
    try:
        image = QPixmap(file_path)
        image = image.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        return image
    except Exception as e:
        print(f"Error loading image from path {file_path}: {e}")
        return QPixmap()

# Function to create labels for product information
def create_labels_for_product(layout, product):
    # Display information about each product
    brand = product.get('product_brand', '')
    name = product.get('product_name', '')
    price = product.get('product_price', '')
    info_label = QLabel(f"Brand: {brand}\nName: {name}\nPrice: {price}")
    layout.addWidget(info_label)

# Function to load and display web images with clickable links
def load_and_display_web_image(layout, product):
    url = product.get('product_url', '')
    img_url = product.get('product_img_url', '')

    def open_product_url(event):
        if url:
            open_url(url)

    web_photo = load_web_image(img_url, size=(120, 120))
    image_label = QLabel()
    image_label.setPixmap(web_photo)
    image_label.mousePressEvent = lambda event: open_product_url(event)
    layout.addWidget(image_label)


# Function that creates the output window with a table
def create_output_window(input_product_name, products):
    app = QApplication([])
    
    # Making window
    window = QWidget()
    window.setWindowTitle("Output Screen")
    window.resize(800, 600)  # Setting window size

    # Create a main layout
    main_layout = QVBoxLayout(window)

    # Create a table widget
    table = QTableWidget()
    table.setColumnCount(4)  # Number of columns: Logo, Image, Product Info, Price
    table.setHorizontalHeaderLabels(['Logo', 'Image', 'Product Info', 'Price'])
    table.setRowCount(len(products))  # Number of rows
    # Correctly pass 'products' to the lambda function
    table.cellClicked.connect(lambda row, column: on_cell_clicked(row, column, products))


    for i, product in enumerate(products):
        # Load and display company logo
        logo_path = product.get('logo_path', '')
        logo_photo = load_image(logo_path, size=(60, 60))
        logo_label = QLabel()
        logo_label.setPixmap(logo_photo)
        logo_label.setAlignment(Qt.AlignCenter)
        table.setCellWidget(i, 0, logo_label)

        # Load and display product image
        img_url = product.get('product_img_url', '')
        img_photo = load_web_image(img_url, size=(120, 120))
        image_label = QLabel()
        image_label.setPixmap(img_photo)
        image_label.setAlignment(Qt.AlignCenter)
        table.setCellWidget(i, 1, image_label)

        # Display product information
        brand = product.get('product_brand', '')
        name = product.get('product_name', '')
        info_label = QLabel(f"Brand: {brand}\nName: {name}")
        info_label.setAlignment(Qt.AlignLeft)
        table.setCellWidget(i, 2, info_label)

        # Display product price
        price = product.get('product_price', '')
        price_label = QLabel(price)
        price_label.setAlignment(Qt.AlignRight)
        table.setCellWidget(i, 3, price_label)

        # Adjust row height to fit content
        table.setRowHeight(i, 120)  # Set row height. Adjust this value as needed.

    # Adjust column widths to fit content
    table.setColumnWidth(0, 130)  # Logo column width
    table.setColumnWidth(1, 130)  # Image column width
    table.setColumnWidth(2, 200)  # Product Info column width
    table.setColumnWidth(3, 100)  # Price column width

    # ... [rest of the code]
  # Add table to the main layout
    main_layout.addWidget(table)
    window.show()
    app.exec_()

# Function that creates the output window with a scroll area
def on_cell_clicked(row, column, products):
    if column == 1:  # Assuming the second column is the image column
        product_url = products[row].get('product_url', '')
        if product_url:
            open_url(product_url)


# Example usage
if __name__ == '__main__':
    # Example data
    products = [
        {'product_brand': 'Brand1', 'product_name': 'Product1', 'product_price': '$10', 'product_url': 'http://example.com', 'product_img_url': 'http://example.com/image.jpg', 'logo_path': 'logo1.jpg'},
        # Add more product dictionaries here...
    ]
    create_output_window('Example Product', products)