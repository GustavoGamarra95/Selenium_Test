import logging
import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


def setup_browser(browser_name, headless):

    logger.info(f"Configurando navegador: {browser_name}, headless: {headless}")
    if browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(
            service=Service(GeckoDriverManager().install()), options=options
        )
    elif browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    else:
        logger.error(f"Navegador no soportado: {browser_name}")
        raise ValueError(f"Navegador no soportado: {browser_name}")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = setup_browser(browser, headless)
    driver.get(os.getenv("BASE_URL", "https://www.saucedemo.com"))
    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)
    driver.find_element_by_class_name("shopping_cart_link").click()
    cart_page = CartPage(driver)
    cart_page.click_checkout()
    logger.info(f"Iniciando prueba de checkout con navegador: {browser}")
    yield driver
    logger.info("Cerrando navegador")
    driver.quit()


def take_screenshot(driver, test_name):
    """Toma una captura de pantalla y la guarda en reports/screenshots/ con timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "reports/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    logger.info(f"Captura guardada: {screenshot_path}")
    return screenshot_path


@pytest.mark.parametrize(
    "first_name,last_name,zip_code,expected_error",
    [
        ("John", "Doe", "12345", ""),
        ("", "", "", "First Name is required"),
        ("John", "Doe", "invalid", "Error"),
    ],
)
def test_checkout_scenarios(
    driver, request, first_name, last_name, zip_code, expected_error
):
    logger.info(f"Probando checkout con nombre: {first_name}, apellido: {last_name}")
    checkout_page = CheckoutPage(driver)
    checkout_page.enter_details(first_name, last_name, zip_code)
    checkout_page.click_continue()
    error_message = checkout_page.get_error_message()
    if error_message:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Mensaje de error encontrado: {error_message}, captura: {screenshot_path}"
        )
    if not expected_error:
        checkout_page.click_finish()
        assert (
            "Thank you for your order!" in checkout_page.get_complete_message()
        ), "Checkout no completado"
    else:
        assert (
            expected_error in error_message
        ), f"Error esperado: {expected_error}, obtenido: {error_message}"
