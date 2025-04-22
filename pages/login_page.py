from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")

        def enter_username(self, username):
            self.driver.find_element(*self.username_input).send_keys(username)

        def enter_password(self, password):
            self.driver.find_element(*self.password_input).send_keys(password)

        def click_login(self):
            self.driver.find_element(*self.login_button).click()

        def get_error_message(self):
            try:
                return self.driver.find_element(*self.error_message).text
            except:
                return ""
