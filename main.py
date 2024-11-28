import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SvetparsSpider:
    def __init__(self):
        # Настройка драйвера
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.start_url = "https://www.divan.ru/category/svet"
        self.lamps_data = []  # Список для хранения данных о лампах

    def parse(self):
        # Открываем страницу
        self.driver.get(self.start_url)

        # Ожидаем, пока элементы не будут загружены
        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.LlPhw')))

        # Найдем все элементы, содержащие информацию о лампах
        lamps = self.driver.find_elements(By.CSS_SELECTOR, 'div.LlPhw')

        # Собираем данные
        for lamp in lamps:
            try:
                name = lamp.find_element(By.CSS_SELECTOR, 'div.lsooF span').text
            except:
                name = "Неизвестное название"

            try:
                price = lamp.find_element(By.CSS_SELECTOR, 'div.pY3d2 span.ui-LD-ZU.KIkOH').text
            except:
                price = "Неизвестная цена"

            try:
                url = lamp.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            except:
                url = "Нет ссылки"

            # Добавляем данные в список
            self.lamps_data.append({
                'Название люстры': name,
                'Цена': price,
                'Ссылка на товар': url
            })

    def save_to_csv(self):
        # Сохраняем данные в CSV файл
        with open("lamps.csv", 'w', newline='', encoding='utf-8-sig') as file:
            # Определяем порядок столбцов
            fieldnames = ['Название люстры', 'Цена', 'Ссылка на товар']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Записываем заголовки
            writer.writerows(self.lamps_data)  # Записываем все данные из списка

    def close(self):
        # Закрываем браузер после выполнения
        self.driver.quit()

# Создаем объект паука и запускаем парсинг
spider = SvetparsSpider()
spider.parse()
spider.save_to_csv()  # Сохраняем данные в файл CSV
spider.close()
