import logging
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)
logger.info("Configurando pruebas de inventario")


@pytest.fixture
def driver(request, driver):  # Usa la fixture driver de conftest.py
    login_page = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(login_page.username_input)
    )
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    logger.info(f"Iniciando prueba de inventario")
    yield driver


@pytest.mark.inventory
def test_inventory_page_loads(driver, request):
    """Verifica que la página de inventario cargue correctamente."""
    inventory_page = InventoryPage(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(inventory_page.title)
        )
        title = inventory_page.get_page_title()
        assert title == "Products", f"Título esperado 'Products', obtenido '{title}'"
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Error en test_inventory_page_loads: {str(e)}, captura: {screenshot_path}"
        )
        raise


@pytest.mark.inventory
def test_inventory_item_count(driver, request):
    """Verifica que la página de inventario muestre 6 ítems."""
    inventory_page = InventoryPage(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(inventory_page.inventory_items)
        )
        items = inventory_page.get_inventory_items()
        assert len(items) == 6, f"Esperado 6 ítems, encontrado {len(items)}"
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Error en test_inventory_item_count: {str(e)}, captura: {screenshot_path}"
        )
        raise


@pytest.mark.inventory
@pytest.mark.parametrize(
    "sort_option,expected_first_item",
    [
        ("Name (A to Z)", "Sauce Labs Backpack"),
        ("Name (Z to A)", "Test.allTheThings() T-Shirt (Red)"),
        ("Price (low to high)", "Sauce Labs Onesie"),
        ("Price (high to low)", "Sauce Labs Fleece Jacket"),
    ],
)
def test_sort_inventory(driver, request, sort_option, expected_first_item):
    """Prueba el ordenamiento de productos en la página de inventario."""
    inventory_page = InventoryPage(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(inventory_page.sort_dropdown)
        )
        inventory_page.sort_by(sort_option)
        items = inventory_page.get_inventory_items()
        first_item_name = (
            items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        )

        assert first_item_name == expected_first_item, (
            f"Esperado '{expected_first_item}' como primer ítem para '{sort_option}', "
            f"obtenido '{first_item_name}'"
        )
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Error en test_sort_inventory: {str(e)}, captura: {screenshot_path}"
        )
        raise


@pytest.mark.inventory
def test_add_item_to_cart(driver, request):
    """Prueba agregar un ítem al carrito desde la página de inventario."""
    inventory_page = InventoryPage(driver)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(inventory_page.inventory_items)
        )
        inventory_page.add_item_to_cart(0)
        cart_count = inventory_page.get_cart_count()
        assert (
            cart_count == "1"
        ), f"Esperado 1 ítem en el carrito, obtenido {cart_count}"
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Error en test_add_item_to_cart: {str(e)}, captura: {screenshot_path}"
        )
        raise
