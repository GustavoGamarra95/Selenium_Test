from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.title = (By.CLASS_NAME, "title")
        self.inventory_items = (By.CLASS_NAME, "inventory_item")
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")
        self.cart_count = (By.CLASS_NAME, "shopping_cart_badge")
    
    def get_page_title(self):
        return self.driver.find_element(*self.title).text
    
    def get_inventory_items(self):
        return self.driver.find_elements(*self.inventory_items)
    
    def sort_by(self, option):
        select = Select(self.driver.find_element(*self.sort_dropdown))
        select.select_by_visible_text(option)
    
    def add_item_to_cart(self, index):
        items = self.get_inventory_items()
        items[index].find_element_by_css_selector("[data-test^='add-to-cart']").click()
    
    def get_cart_count(self):
        try:
            return self.driver.find_element(*self.cart_count).text
        except:
            return "0"