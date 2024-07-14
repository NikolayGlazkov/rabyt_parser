from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

def log_message(message):
    print(f"[INFO] {message}")

def get_info_from_efrsb_massage(massage_number, lot_numbers):
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
        
        # Поиск лота в списке лотов
        html = driver.page_source

        print(html)

        soup = BeautifulSoup(html, 'html.parser')
        lot_dict = {}
        rows = soup.select('table.lotInfo tbody tr')[1:]

        # Проход по всем строкам и извлечение данных
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                lot_num = cols[0].text.strip()  # lot_number уже используется как аргумент функции
                if lot_num in lot_numbers:
                    lot_name = cols[1].text.strip()
                    lot_dict[lot_num] = lot_name

        # Добавление lot_dict как вложенного словаря в result_dict
        result_dict["lots"] = lot_dict
        
        return result_dict




def oll_info(my_dict: dict):
    result_keys = [
        '№ сообщения', 
        ('Наименование должника', 'ФИО должника'), 
        ('Адрес',"Место жительства"),
        ('ОГРН',"СНИЛС"),
        'ИНН', 
        'Арбитражный управляющий', 
        'Адрес для корреспонденции', 
        'E-mail', 
        'СРО АУ', 
        'Вид торгов',
        'lots'
    ]
    
    for key in result_keys:
        if isinstance(key, tuple):
            # Для случаев, когда ключи могут быть разные
            for subkey in key:
                if subkey in my_dict:
                    print(f"{subkey}: {my_dict.get(subkey)}")
                    break
        else:
            print(f"{key}: {my_dict.get(key)}")




def parse_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    email = None
    
    # Поиск email в таблице
    table = soup.find('table', class_='lotInfo')
    if table:
        email_cell = table.find('td', text=re.compile(r'\b[Ee]-?mail\b'))
        if email_cell:
            email = email_cell.find_next('td').get_text(strip=True)
    
    # Поиск email в тексте, если не найден в таблице
    if not email:
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', soup.get_text())
        if email_match:
            email = email_match.group(0)
    
    # Если email отсутствует
    if not email:
        email = 'Email отсутствует'
    
    return email

# Пример использования
html_content = '''Ваш HTML-код здесь'''
email = parse_page(html_content)
print(email)
