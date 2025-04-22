import logging.config

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Configurando pruebas de inventario")


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
    logger.info(f"Iniciando prueba de inventario con navegador: {browser}")
    yield driver
    logger.info("Cerrando navegador")
    driver.quit()


def test_inventory_page_loads(driver):
    inventory_page = InventoryPage(driver)
    assert (
        inventory_page.get_page_title() == "Products"
    ), "Título de página de inventario incorrecto"


def test_inventory_item_count(driver):
    inventory_page = InventoryPage(driver)
    items = inventory_page.get_inventory_items()
    assert len(items) == 6, f"Esperado 6 ítems, encontrado {len(items)}"


@pytest.mark.parametrize(
    "sort_option,expected_order",
    [
        ("Name (A to Z)", lambda x: x),
        ("Name (Z to A)", lambda x: sorted(x, reverse=True)),
        ("Price (low to high)", lambda x: sorted(x, key=float)),
        ("Price (high to low)", lambda x: sorted(x, key=float, reverse=True)),
    ],
)
def test_sort_inventory(driver, sort_option, expected_order):
    inventory_page = InventoryPage(driver)
    inventory_page.sort_by(sort_option)
    items = inventory_page.get_inventory_items()
    if "Name" in sort_option:
        names = [
            item.find_element_by_class_name("inventory_item_name").text
            for item in items
        ]
        assert names == expected_order(names), f"Ítems no ordenados por {sort_option}"
    else:
        prices = [
            float(
                item.find_element_by_class_name("inventory_item_price").text.replace(
                    "$", ""
                )
            )
            for item in items
        ]
        assert prices == expected_order(prices), f"Ítems no ordenados por {sort_option}"


def test_add_item_to_cart(driver):
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart(0)
    cart_count = inventory_page.get_cart_count()
    assert cart_count == "1", "Ítem no añadido al carrito"
