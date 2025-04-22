import os
import sys
import logging
import logging.config
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# Agregar el directorio padre al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configuración del logging
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)
logger.info("Configurando pruebas de inventario")

def setup_browser(browser_name, headless):
    """Configura el navegador según el nombre y modo headless."""
    logger.info(f"Configurando navegador: {browser_name}, headless: {headless}")
    if browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
    elif browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
    else:
        logger.error(f"Navegador no soportado: {browser_name}")
        raise ValueError(f"Navegador no soportado: {browser_name}")

@pytest.fixture
def driver(request):
    """Fixture para inicializar y cerrar el navegador."""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = setup_browser(browser, headless)
    driver.get(os.getenv("BASE_URL", "https://www.saucedemo.com"))

    # Login con standard_user
    login_page = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(login_page.username_input)
    )
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    logger.info(f"Iniciando prueba de inventario con navegador: {browser}, headless: {headless}")
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
        logger.error(f"Error en test_inventory_page_loads: {str(e)}, captura: {screenshot_path}")
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
        logger.error(f"Error en test_inventory_item_count: {str(e)}, captura: {screenshot_path}")
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
        first_item_name = items[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        
        assert first_item_name == expected_first_item, (
            f"Esperado '{expected_first_item}' como primer ítem para '{sort_option}', "
            f"obtenido '{first_item_name}'"
        )
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(f"Error en test_sort_inventory: {str(e)}, captura: {screenshot_path}")
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
        assert cart_count == "1", f"Esperado 1 ítem en el carrito, obtenido {cart_count}"
    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(f"Error en test_add_item_to_cart: {str(e)}, captura: {screenshot_path}")
        raise