import pytest

def pytest_addoption(parser):
    """Registra opciones personalizadas para pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador para las pruebas: chrome o firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar pruebas en modo headless"
    )