from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import keyboard
from chromedriver_py import binary_path
from helpers import pressTabAndThenDownArrowUntil, getAdsData

def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--window-size=1280,720")
    return options

def human_type(element, text, driver):
    """Escritura ultra realista con variabilidad mejorada"""
    actions = ActionChains(driver)
    for char in text:
        # Retardo variable aumentado
        time.sleep(random.uniform(0.15, 0.65))
        element.send_keys(char)
        
        # Movimientos de mouse más complejos
        actions.move_by_offset(
            random.randint(-12, 12),
            random.randint(-12, 12)
        ).perform()
        
        # 20% de probabilidad de corrección
        if random.random() < 0.2 and len(text) > 3:
            for _ in range(random.randint(1, 2)):
                element.send_keys(Keys.BACK_SPACE)
                time.sleep(random.uniform(0.2, 0.5))
            element.send_keys(char)
    
    # Pausa final extendida
    time.sleep(random.uniform(1.0, 2.5))

def human_delay(min_t, max_t=None):
    """Esperas más largas y naturales"""
    delay = random.uniform(min_t, max_t if max_t else min_t * 2.5)
    time.sleep(delay * random.uniform(0.8, 1.2))

def simulate_human_interaction(element, driver):
    """Interacción realista con elementos"""
    actions = ActionChains(driver)
    
    # Movimiento de aproximación en zig-zag
    for _ in range(3):
        actions.move_by_offset(
            random.randint(-8, 8),
            random.randint(-8, 8)
        ).pause(random.uniform(0.1, 0.3))
    
    actions.move_to_element(element)
    actions.pause(random.uniform(0.3, 1.0))
    actions.perform()

def startPostingAds():
    driver = webdriver.Chrome(
        service=webdriver.ChromeService(binary_path),
        options=get_chrome_options()
    )
    
    try:
        adsList = getAdsData()
        driver.implicitly_wait(15)

        for ad_index, adData in enumerate(adsList):
            try:
                # Espera inicial progresiva
                human_delay(ad_index * 2 + 5, ad_index * 2 + 10)
                
                # Navegación con delays variables
                driver.get('https://www.facebook.com/marketplace/create/item')
                human_delay(3.5, 7.0)

                # Flujo de publicación con tiempos mejorados
                photo = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Add Photos']"))
                )
                simulate_human_interaction(photo, driver)
                photo.click()
                human_delay(2.5, 4.0)
                keyboard.write(adData['image'])
                human_delay(1.5, 2.5)
                keyboard.press('enter')
                human_delay(4.0, 6.0)

                # Secuencia de llenado de campos
                title = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Title']"))
                )
                simulate_human_interaction(title, driver)
                human_type(title, adData['title'], driver)
                human_delay(1.2, 2.8)

                price = driver.find_element(By.XPATH, "//*[@aria-label='Price']")
                simulate_human_interaction(price, driver)
                human_type(price, adData['price'], driver)
                human_delay(1.5, 3.0)

                # ... (Resto de campos con misma estructura)

                # Publicación final con espera extendida
                publishButton = WebDriverWait(driver, 25).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.buofh1pr.rj1gh0hx > div[role="button"]'))
                )
                simulate_human_interaction(publishButton, driver)
                human_delay(3.0, 5.0)
                publishButton.click()
                print(f"Anuncio publicado: {adData['title']}")
                human_delay(15.0, 25.0)  # Espera crítica entre anuncios

            except Exception as e:
                print(f"Error: {str(e)[:100]}...")
                human_delay(15.0, 30.0)  # Recuperación ante errores
                continue

    finally:
        driver.quit()