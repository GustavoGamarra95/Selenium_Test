import logging
from datetime import datetime
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


@pytest.mark.login
@pytest.mark.parametrize(
    "username,expected_error",
    [
        ("standard_user", ""),
        ("locked_out_user", "Epic sadface: Sorry, this user has been locked out."),
        ("problem_user", ""),
        ("performance_glitch_user", ""),
        ("error_user", ""),
        ("visual_user", ""),
        (
            "invalid_user",
            "Epic sadface: Username and password do not match any user in this service",
        ),
        ("", "Epic sadface: Username is required"),
    ],
)
def test_login_scenarios(driver, request, username, expected_error):
    """Prueba escenarios de login para diferentes usuarios."""
    logger.info(f"Probando login con usuario: {username}")
    login_page = LoginPage(driver)

    try:
        # Esperar a que el campo de usuario esté visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(login_page.username_input)
        )

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
            "standard_user",
            "problem_user",
            "error_user",
            "visual_user",
            "performance_glitch_user",
        ]:
            assert driver.current_url.endswith(
                "/inventory.html"
            ), f"{username} no redirigió a inventario"
        else:
            assert (
                error_message == expected_error
            ), f"Error esperado: '{expected_error}', obtenido: '{error_message}'"

    except Exception as e:
        screenshot_path = take_screenshot(driver, request.node.name)
        logger.error(f"Error durante la prueba: {str(e)}, captura: {screenshot_path}")
        raise
