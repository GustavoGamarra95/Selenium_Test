from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object Model para la página de login de saucedemo.com"""

    # Localizadores
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.CSS_SELECTOR, "div.error-message-container.error")

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        """Ingresa el nombre de usuario en el campo correspondiente."""
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)

    def enter_password(self, password):
        """Ingresa la contraseña en el campo correspondiente."""
        self.driver.find_element(*self.password_input).send_keys(password)

    def click_login(self):
        """Hace clic en el botón de login."""
        self.driver.find_element(*self.login_button).click()

    def get_error_message(self):
        """Obtiene el mensaje de error, si está presente."""
        try:
            return (
                WebDriverWait(self.driver, 5)
                .until(EC.visibility_of_element_located(self.error_message))
                .text
            )
        except:
            return ""
