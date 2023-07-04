import csv
import time
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

def scrape_page(driver):
    data = []

    element_path = ".//div[@class='card property-card shadow']"
    elements = driver.find_elements(By.XPATH, element_path)

    for element in elements:
        address =""
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
            #agent_name_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH, './/*[contains(@class, "pe-2 mt-2 fs-5 d-none d-xl-block ng-star-inserted")]')))
            agent_name = agent_name_element.get_attribute("textContent").strip()
            
        except NoSuchElementException:
            pass

        try:
            price_element = element.find_element(By.XPATH, './/*[contains(@class,"card-title")]')
            #price_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@class,"card-title fs-1")]')))
            price = price_element.get_attribute("textContent").strip()
        except NoSuchElementException:
            pass

        try:
            link_element = element.find_element(By.XPATH, './/a')
            #link_element = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH, './/a')))
            link = link_element.get_attribute("href").strip()
        except NoSuchElementException:
            pass

        print(f"Address:{address},Agent Name: {agent_name}, Price: {price}, Link: {link}")
        data.append([address,agent_name, price, link])

    return data

def navigate_to_next_page(driver):
    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@class="pagination-next ng-star-inserted"]/a')))
        driver.execute_script("arguments[0].click();", next_button)

        WebDriverWait(driver, 20).until(EC.staleness_of(next_button))
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
        driver.implicitly_wait(20)

        driver.get("https://www.myhome.ie/")

        handle_cookies(driver)

        time.sleep(5)
        search_button = driver.find_element(By.XPATH, '/html/body/app-root/div/app-home/div/div/div[1]/div/div[1]/div/div/div/div/app-home-search-form-container/div/app-base-search-form/div/div[6]')
        search_button.click()

        #WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mh-modal-body"]/div/div/fa-icon'))).click()

        page = 1
        while True:
            print("Scraping Page:", page)

            try:
                data = scrape_page(driver)
                if len(data) == 0:
                    break

                with open('myhome_web111.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)

                navigate_to_next_page(driver)

                page += 1

            except Exception as e:
                print("An error occurred while scraping page:", str(e))
                continue
            #time.sleep(5)  # Wait for 5 seconds between each page

    finally:
        time.sleep(20)
        driver.quit()

if __name__ == '__main__':
    main()
