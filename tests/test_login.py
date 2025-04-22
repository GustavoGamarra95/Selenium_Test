import logging
import logging.config
import os
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from pages.login_page import LoginPage

# Configuración del logging
logging.config.fileConfig("logging_conf")
logger = logging.getLogger(__name__)


def setup_browser(browser_name, headless):
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
            options.add_argument("--headless")
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
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
    logger.info(f"Iniciando prueba con navegador: {browser}, headless: {headless}")
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
    "username,expected_error",
    [
        ("standard_user", ""),
        ("locked_out_user", "Sorry, this user has been locked out"),
        ("problem_user", ""),
        ("performance_glitch_user", ""),
        ("error_user", ""),
        ("visual_user", ""),
        ("invalid_user", "Username and password do not match"),
        ("", "Username is required"),
    ],
)
def test_login_scenarios(driver, request, username, expected_error):
    logger.info(f"Probando login con usuario: {username}")
    login_page = LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password("secret_sauce")
    login_page.click_login()
    error_message = login_page.get_error_message()

    if error_message:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(
            f"Mensaje de error encontrado: {error_message}, captura: {screenshot_path}"
        )

    if not expected_error and username in [
        "problem_user",
        "error_user",
        "visual_user",
        "performance_glitch_user",
    ]:
        assert driver.current_url.endswith(
            "/inventory.html"
        ), f"{username} no redirigió a inventario"

    assert (
        error_message == expected_error
    ), f"Error esperado: {expected_error}, obtenido: {error_message}"
