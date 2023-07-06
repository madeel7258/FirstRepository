import csv
import time
import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def handle_cookies(driver):
    try:
        cookies_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        cookies_option.click()
    except TimeoutException:
        pass

import datetime

def scrape_page(driver):
    data = []

    element_path = ".//div[@class='card property-card shadow']"
    elements = driver.find_elements(By.XPATH, element_path)

    for element in elements:
        address = ""
        agent_name = ""
        price = ""
        link = ""

        try:
            address_element = element.find_element(By.XPATH, './/h3[contains(@class,"card-text mt-4")]')
            address = address_element.get_attribute("textContent").strip()

        except NoSuchElementException:
            pass

        try:
            agent_name_element = element.find_element(By.XPATH, './/*[contains(@class,"pe-2 mt-2 fs-5 d-none d-xl-block")]')
            agent_name = agent_name_element.get_attribute("textContent").strip()

        except NoSuchElementException:
            pass

        try:
            price_element = element.find_element(By.XPATH, './/*[contains(@class,"card-title")]')
            price = price_element.get_attribute("textContent").strip()
        except NoSuchElementException:
            pass

        try:
            link_element = element.find_element(By.XPATH, './/a')
            link = link_element.get_attribute("href").strip()
        except NoSuchElementException:
            pass

        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Scraped at: {current_time_str}, Address: {address}, Agent Name: {agent_name}, Price: {price}, Link: {link}")
        data.append([current_time_str, address, agent_name, price, link])

    return data


def navigate_to_next_page(driver, page):
    try:
        next_url = f"https://www.myhome.ie/residential/ireland/property-for-sale?page={page}"
        driver.get(next_url)

        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="card property-card shadow"]')))
        return True

    except (NoSuchElementException, TimeoutException) as e:
        print("An error occurred while navigating to the next page:", str(e))
        return False

def main():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        

        driver.get("https://www.myhome.ie/residential/ireland/property-for-sale")

        handle_cookies(driver)

        time.sleep(5)
        #search_button = driver.find_element(By.XPATH, '/html/body/app-root/div/app-home/div/div/div[1]/div/div[1]/div/div/div/div/app-home-search-form-container/div/app-base-search-form/div/div[6]')
        #search_button.click()
        previous_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@class="pagination-next"]/preceding-sibling::li[1]')))
        page_text = previous_button.text.strip()
        max_page = int(''.join(filter(str.isdigit, page_text)))
        print("Maximum Page Number:", max_page)
        
        print(type(max_page))
        print("Maximum Page Number:=============== ", max_page)

        for page in range(1, max_page):
            print("Scraping Page:", page)

            try:
                data = scrape_page(driver)
                if len(data) == 0:
                    break

                with open('myhome_web-scrape.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if page == 1:
                        writer.writerow(['time', 'address', 'agent', 'price', 'link'])                    
                    writer.writerows(data)
                navigate_to_next_page(driver, page)

            except Exception as e:
                print("An error occurred while scraping page:", str(e))
                continue

            time.sleep(10)  # Wait for 5 seconds between each page

    finally:
        time.sleep(20)
        driver.quit()

if __name__ == '__main__':
    main()