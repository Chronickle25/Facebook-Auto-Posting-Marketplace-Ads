from selenium import webdriver
from chromedriver_py import binary_path

def init_driver():
    """Inicializa y devuelve el WebDriver de Chrome."""
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=webdriver.ChromeService(binary_path), options=chrome_options)
    driver.maximize_window()
    return driver

# Instancia única del WebDriver
driver = init_driver()
