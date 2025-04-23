import logging
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.fixture
def driver(request, driver):  # Usa la fixture driver de conftest.py
    login_page = LoginPage(driver)
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    cart_page = CartPage(driver)
    cart_page.click_checkout()

    logger.info(f"Iniciando prueba de checkout")
    yield driver


@pytest.mark.parametrize(
    "first_name,last_name,zip_code,expected_error",
    [
        ("John", "Doe", "12345", ""),
        ("", "", "", "Error: First Name is required"),
        ("John", "", "", "Error: Last Name is required"),
        ("John", "Doe", "", "Error: Postal Code is required"),
    ],
)
def test_checkout_scenarios(
    driver, request, first_name, last_name, zip_code, expected_error
):
    logger.info(
        f"Probando checkout con nombre: {first_name}, apellido: {last_name}, ZIP: {zip_code}"
    )
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
        complete_message = checkout_page.get_complete_message()
        assert (
            "Thank you for your order!" in complete_message
        ), "Checkout no fue completado correctamente"
    else:
        assert (
            expected_error == error_message
        ), f"Se esperaba: '{expected_error}', pero se obtuvo: '{error_message}'"
