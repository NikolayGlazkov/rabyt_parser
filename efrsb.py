from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def log_message(message):
    print(f"[INFO] {message}")

def get_info_from_efrsb_massage(massage_number,lot_number):
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 10)
        
        driver.get('https://old.bankrot.fedresurs.ru/Default.aspx')
        
        # Ожидание и клик по ссылке "Сообщения"
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_lnkMessages"]'))).click()
        
        # Ввод номера сообщения
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphBody_tbMessageNumber"]'))).send_keys(massage_number)
        
        # Очистка даты и клик по кнопке поиска
        
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_cphBody_cldrBeginDate_tbSelectedDate"]'))).clear()
        
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_cphBody_ibMessagesSearch"]'))).click()
        time.sleep(1)
        # Ожидание загрузки результатов поиска
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Объявление о проведении торгов'))).click()
        
        # Ожидание открытия нового окна
       
        
        # Получение дескриптора текущего окна
        current_window = driver.current_window_handle
        
        # Получение дескрипторов всех окон
        all_windows = driver.window_handles
        
        # Поиск дескриптора нового окна
        for window in all_windows:
            if window != current_window:
                new_window = window
                break
        
        # Переключение на новое окно
        driver.switch_to.window(new_window)
        time.sleep(1)
        # Ожидание загрузки нового окна
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'primary')))
        
        # Получение URL нового окна
        new_url = driver.current_url
        print(new_url)
        driver.get(new_url)
        time.sleep(1)
        # Поиск всех элементов с классом 'primary'
        primary_elements = driver.find_elements(By.CLASS_NAME, 'primary')
        
        if not primary_elements:
            log_message("No primary elements found.")
            return
        
        log_message(f"Found {len(primary_elements)} primary elements.")
        
        # Инициализация словаря для хранения результатов
        result_dict = {}

        for primary in primary_elements:
            try:
                # Получение текста первичного элемента
                key = primary.text.strip()
                
                # Поиск следующего элемента-соседа, чтобы получить значение (предполагается, что значение находится в следующем элементе-соседе)
                value_element = primary.find_element(By.XPATH, 'following-sibling::td')
                value = value_element.text.strip()

                # Добавление пары ключ-значение в словарь
                result_dict[key] = value

            except Exception as e:
                log_message(f"Error processing element: {e}")
        # поиск лота в списке лотов
        # lot_list = driver.find_elements(By.CLASS_NAME,'lotInfo')
        # for i in lot_list:
        #     print(i.find_element(By.CLASS_NAME,'odd').text)
        return result_dict
        
        # Закрытие нового окна и переключение обратно на исходное окно (если необходимо)
        # driver.close()
        # driver.switch_to.window(current_window)
def OOO_info(my_dict: dict):
    result_key = ['№ сообщения', 'Наименование должника', 'Адрес', 'ОГРН', 'ИНН', 'Арбитражный управляющий', "Адрес для корреспонденции", "E-mail", "СРО АУ"]
    for key in result_key:
        print(f"{key}: {my_dict.get(key)}")
        
print(get_info_from_efrsb_massage("14806880","1"))