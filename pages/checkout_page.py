from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.title = (By.CLASS_NAME, "title")
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.zip_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.complete_message = (By.CLASS_NAME, "complete-header")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")
    
    def get_page_title(self):
        return self.driver.find_element(*self.title).text
    
    def enter_details(self, first_name, last_name, zip_code):
        self.driver.find_element(*self.first_name).send_keys(first_name)
        self.driver.find_element(*self.last_name).send_keys(last_name)
        self.driver.find_element(*self.zip_code).send_keys(zip_code)
    
    def click_continue(self):
        self.driver.find_element(*self.continue_button).click()
    
    def click_finish(self):
        self.driver.find_element(*self.finish_button).click()
    
    def get_complete_message(self):
        return self.driver.find_element(*self.complete_message).text
    
    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_message).text
        except:
            return ""