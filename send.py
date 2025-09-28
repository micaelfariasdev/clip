from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
def send(arq, descricao):
    print(arq)

    numero = 5586981569018

    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")  # útil para headless
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-data-dir=/tmp/chrome-whatsapp-profile")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"https://web.whatsapp.com/send?phone={numero}&text=&app_absent=0")

    wait = WebDriverWait(driver, 60)


    for a in arq:
        a = f'{root_dir}/{a}'
        print(a)
        clip_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[1]/button')))
        clip_button.click()
        media_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/span[6]/div/ul/div/div/div[1]/li/div/input')))

        time.sleep(1)
        media_input.send_keys(a)
        time.sleep(1)
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]')))
        send_btn.click()
        time.sleep(1)


    try:
        WebDriverWait(driver, 320).until_not(
        EC.presence_of_element_located((By.XPATH, '//span[@data-visualcompletion="loading-state"]'))
    )
    except:
        print("Spinner não encontrado ou já sumiu")



    msg_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")))
    msg_box.send_keys(descricao)
    msg_box.send_keys(Keys.ENTER)


    print("Vídeo enviado!")
    time.sleep(5)
    driver.quit()
