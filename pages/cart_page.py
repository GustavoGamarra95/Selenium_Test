from selenium.webdriver.common.by import By


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.title = (By.CLASS_NAME, "title")
        self.cart_items = (By.CLASS_NAME, "cart_item")
        self.continue_shopping_button = (By.ID, "continue-shopping")
        self.checkout_button = (By.ID, "checkout")

    def get_page_title(self):
        return self.driver.find_element(*self.title).text

    def get_cart_items(self):
        return self.driver.find_elements(*self.cart_items)

    def remove_item(self, index):
        items = self.get_cart_items()
        # Actualizo este método para usar la API más reciente de Selenium
        items[index].find_element(By.CSS_SELECTOR, "[data-test^='remove']").click()

    def click_continue_shopping(self):
        self.driver.find_element(*self.continue_shopping_button).click()

    def click_checkout(self):
        self.driver.find_element(*self.checkout_button).click()
