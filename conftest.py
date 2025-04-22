import os
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

# Configuración del logging
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def pytest_addoption(parser):
    """Registra opciones personalizadas para pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        help="Navegador a usar: chrome o firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar en modo headless",
    )

def pytest_configure():
    """Configura el logging al inicio de la sesión de pytest."""
    logging.config.fileConfig("logging.conf")

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

def take_screenshot(driver, test_name):
    """Toma una captura de pantalla y la guarda en reports/screenshots/ con timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = "reports/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    logger.info(f"Captura guardada: {screenshot_path}")
    return screenshot_path

@pytest.fixture
def driver(request):
    """Fixture para inicializar y cerrar el navegador."""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver = setup_browser(browser, headless)
    driver.get(os.getenv("BASE_URL", "https://www.saucedemo.com"))
    logger.info(f"Iniciando prueba con navegador: {browser}, headless: {headless}")
    yield driver
    logger.info("Cerrando navegador")
    driver.quit()