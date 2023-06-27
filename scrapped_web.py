import csv
import time
import random
from test_proxy import check_proxies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def handle_cookies(driver):
    try:
        cookies_option = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/main/div/button[2]')))
        cookies_option.click()
    except:
        pass


def scrape_data(driver, link):
    driver.get(link)
    time.sleep(10)
    element_path='//*[contains(@class, "SearchPage__Result-gg133s-2")]'
    elements = driver.find_elements(By.XPATH, element_path)

    data = []

    for element in elements:
        has_error = False

        try:
            agent_xpath='.//span[@data-testid="agent-name"]'
            agent_name_element = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.XPATH, agent_xpath)))
            agent_name = agent_name_element.get_attribute("textContent")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            has_error = True

        try:
            price_xpath='.//*[@data-testid="price"]'
            price_element = WebDriverWait(element, 10).until(
                EC.presence_of_element_located((By.XPATH,price_xpath )))
            price = price_element.get_attribute("textContent")
            print(f"Agent Name: {agent_name}, Price: {price}")
            data.append({'Agent Name': agent_name, 'Price': price})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            has_error = True

        if has_error:
            # Perform error handling if needed
            pass

    return data


def save_data_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, keys)
        writer.writerows(data)


def save_links_to_csv(links, filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[link] for link in links])


def main():
    

    # Step 1: Check the working proxies
    working_proxies = check_proxies('proxy_list11.csv')
    print(f"Working Proxies: {working_proxies}")
    print(len(working_proxies))
    driver = webdriver.Chrome()
    # Step 2: Randomly select a working proxy for each page
    proxy_count = len(working_proxies)
    proxy_index = 0
    
    scraped_data = []  # List to store the scraped data
    scraped_links = []  # List to store the scraped links

    # Read the 'scraped_links.csv' file
    with open('scrapped_links.csv', 'r') as scraped_links_file:
        scraped_links_reader = csv.reader(scraped_links_file)
        next(scraped_links_reader)  # Skip the header row in scraped_links.csv

        # Read the scraped links from 'scraped_links.csv' into the scraped_links list
        for row in scraped_links_reader:
            scraped_links.append(row[0])

    # Read the 'city_page_links.csv' file and scrape data for unmatched links
    with open('city_page_links.csv', 'r') as city_links_file:
        city_links_reader = csv.reader(city_links_file)
        next(city_links_reader)  # Skip the header row in city_page_links.csv

        for city_row in city_links_reader:
            link = city_row[0]

            if link in scraped_links:
                print(f"Link '{link}' already scraped. Skipped...")
                continue

            handle_cookies(driver)

            # Step 3: Set the proxy for the driver
            proxy = working_proxies[proxy_index]
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Chrome(options=options)

            data = scrape_data(driver, link)

            scraped_data.extend(data)  # Append scraped data to the main list
            scraped_links.append(link)  # Append the scraped link to the list

            # Save the scraped data and links to CSV files
            save_data_to_csv(scraped_data, 'scrapped_data.csv')
            save_links_to_csv(scraped_links, 'scrapped_links.csv')

            # Open a new browser page or perform any necessary operations
            time.sleep(20)

            # Step 4: Rotate to the next proxy
            proxy = random.choice(working_proxies)

    driver.quit()


if __name__ == '__main__':
    main()
