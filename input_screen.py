from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

class InputScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # This get values function is used to retrieve the values from the widgets
    def get_values(self):
        return self.entry_product_name.text(), self.combo_num_products.currentText(), self.entry_zip_code.text()
    

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Product Name
        self.label_product_name = QLabel("Product Name:")
        self.entry_product_name = QLineEdit()
        layout1.addWidget(self.label_product_name)
        layout1.addWidget(self.entry_product_name)

        # Zip Code
        self.label_zip_code = QLabel("Zip Code:")
        self.entry_zip_code = QLineEdit()
        layout2.addWidget(self.label_zip_code)
        layout2.addWidget(self.entry_zip_code)

        # Number of Products
        self.label_num_products = QLabel("Number of Products:")
        self.combo_num_products = QComboBox()
        self.combo_num_products.addItems([str(i) for i in range(1, 11)])
        layout3.addWidget(self.label_num_products)
        layout3.addWidget(self.combo_num_products)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_click)
        button_layout.addWidget(self.search_button)

        # Add layouts to main layout
        main_layout.addLayout(layout1)
        main_layout.addLayout(layout2)
        main_layout.addLayout(layout3)
        main_layout.addLayout(button_layout)

        # Set main layout
        self.setLayout(main_layout)

    def on_search_click(self):
        # Retrieve values from the widgets
        product_name = self.entry_product_name.text()
        zip_code = self.entry_zip_code.text()
        num_of_products = self.combo_num_products.currentText()

        # You can process the data here or return it
        print(f"Product Name: {product_name}, Zip Code: {zip_code}, Number of Products: {num_of_products}")

        # Close the window
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = InputScreen()
    window.show()
    app.exec_()

