
import logging
import logging.config
import os
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

from pages.login_page import LoginPage

# Configuración del logging
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

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
    logger.info(f"Iniciando prueba de login con navegador: {browser}")
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

@pytest.mark.login
@pytest.mark.parametrize("username,expected_result", [
    ("standard_user", "inventory.html"),  # Login exitoso
    ("locked_out_user", "Epic sadface: Sorry, this user has been locked out."),  # Usuario bloqueado
    ("problem_user", "inventory.html"),  # Login exitoso pero con problemas en la UI
    ("performance_glitch_user", "inventory.html"),  # Login exitoso pero lento
    ("error_user", "inventory.html"),  # Login exitoso pero con errores en acciones
    ("visual_user", "inventory.html"),  # Login exitoso pero con defectos visuales
])
def test_login_scenarios(driver, request, username, expected_result):
    """Prueba escenarios de login para diferentes usuarios."""
    logger.info(f"Probando login con usuario: {username}")
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    error_message = login_page.get_error_message()
    if error_message:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(f"Mensaje de error encontrado: {error_message}, captura: {screenshot_path}")
        assert error_message == expected_result, f"Esperado: {expected_result}, obtenido: {error_message}"
    else:
        current_url = driver.current_url
        assert expected_result in current_url, f"Esperado URL con {expected_result}, obtenido: {current_url}"
