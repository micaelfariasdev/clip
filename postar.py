from selenium.webdriver.common.keys import Keys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import tempfile

root_dir = os.path.dirname(os.path.abspath(__file__))


def upload(video_path, descricao, headless=True, agendado=False):
    video_path_ = f'{root_dir}/{video_path}'
    text = descricao

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-gpu")  # útil para headless
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/snap/bin/chromium"
    service = Service("/home/micaelfarias/clip/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.tiktok.com/login")
    time.sleep(2)
    try:
        with open("TK_cookies_loovemusic.br.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()
        driver.get("https://www.tiktok.com/upload?lang=en")
        print('Login feito')
    except:
        return print('Erro ao fazer login')

    try:
        upload_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        upload_input.send_keys(video_path_)
        print('Arquivo enviado', )
    except Exception as e:
        return print('Erro ao enviar arquivo', video_path_, f"{type(e).__name__} - {e}")
    try:
        desc_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.public-DraftEditor-content')))
        desc_box.clear()
        desc_box.send_keys(text)
        print('Descrição enviada')
    except:
        return print('Erro ao enviar descrição')

    if agendado:
        try:
            span_to_click = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[1]/div/div[2]/label[2]"))
            )

            span_to_click.click()
            timed_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[4]/div[1]/div[4]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/div/div/input"))
            )
            timed_input.click()
            hora = agendado
            h, m = map(int, hora.split(':'))
            m = ((m // 5) * 5)
            m = str(m).zfill(2)
            h = str(h).zfill(2)
            h_selector = (By.XPATH, f"//span[contains(@class, 'tiktok-timepicker-left') and text()='{h}']")
            m_selector = (By.XPATH, f"//span[contains(@class, 'tiktok-timepicker-right') and text()='{m}']")
            cont1_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tiktok-timepicker-time-picker-container'))
            )

            cont2_list = WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tiktok-timepicker-time-scroll-container'))
            )

            for cont1 in cont1_list:
                driver.execute_script("arguments[0].style.height = 'min-content';", cont1)

            for cont2 in cont2_list:
                driver.execute_script("arguments[0].style.height = 'min-content';", cont2)
                driver.execute_script("arguments[0].style.maxHeight = 'none';", cont2)
                driver.execute_script("arguments[0].style.overflow = 'visible';", cont2)

            classe_a_adicionar = 'tiktok-timepicker-is-active'
            hour_select = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(h_selector))
            driver.execute_script("arguments[0].classList.add(arguments[1]);", hour_select, classe_a_adicionar)
            driver.execute_script("arguments[0].scrollIntoView();", hour_select)
            hour_select.click()

            minute_select = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(m_selector))
            driver.execute_script("arguments[0].classList.add(arguments[1]);", minute_select, classe_a_adicionar)
            driver.execute_script("arguments[0].scrollIntoView();", minute_select)
            minute_select.click()

            print('Agendamento feito')
        except Exception as e:
            try:
                draft_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((
                        By.CSS_SELECTOR, "button[data-e2e='save_draft_button']")))
                draft_button.click()
                print('Post foi salvo em rascunho devido a um erro ao fazer agendamento')
                driver.quit()
                return
            except Exception as draft_e:
                print('Erro grave: Não foi possível agendar ou salvar rascunho.')
                print(f'Erro de Agendamento: {type(e).__name__} - {e}')
                print(f'Erro de Rascunho: {type(draft_e).__name__} - {draft_e}')
                driver.quit()
                return

    try:
        publish_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "button[data-e2e='post_video_button']")))
        publish_button.click()

        publish_two_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((
                By.XPATH, "/html/body/div[6]/div/div/div[3]/button[2]/div/div")))
        publish_two_button.click()

        print('Publicado com sucesso')
    except Exception as e:
        return print('Erro ao fazer publicação', f'{type(e).__name__} - {e}')

    driver.quit()


