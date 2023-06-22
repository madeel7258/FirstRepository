#All the links are present in the city_page_links.csv file, starting scrapping each link it save the data in "scrapped_data.csv" file,
#and whose link is scrapped it will save in a seperate file "scrapped_links.csv",
#if we start again, those links are available in a scrapped_links.csv file it mean it already scrapped,and those links are skipped,
#and start from thoose link who are not scrapped yet and save the data in scrapped_data.csv file and links save in scrapped_link.csv file.



import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

scraped_data = []  # List to store the scraped data
scraped_links = []  # List to store the scraped links

# Read the 'scraped_links.csv' file
with open('scraped_links.csv', 'r') as scraped_links_file:
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

        driver.get(link)

        # Handle cookies option if it appears
        try:
            cookies_option = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/main/div/button[2]')))
            cookies_option.click()
        except:
            pass
        time.sleep(10)

        elements = driver.find_elements(By.XPATH, '//*[contains(@class, "SearchPage__Result-gg133s-2")]')

        data = []

        for element in elements:
            has_error = False

            try:
                agent_name_element = WebDriverWait(element, 10).until(
                    EC.presence_of_element_located((By.XPATH, './/span[@data-testid="agent-name"]')))
                agent_name = agent_name_element.get_attribute("textContent")

                price_element = WebDriverWait(element, 10).until(
                    EC.presence_of_element_located((By.XPATH, './/*[@data-testid="price"]')))
                price = price_element.get_attribute("textContent")
                print(f"Agent Name: {agent_name}, Price: {price}")
                data.append({'Agent Name': agent_name, 'Price': price})

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                has_error = True

            if has_error:
                # Perform error handling if needed
                pass

        scraped_data.extend(data)  # Append scraped data to the main list
        scraped_links.append(link)  # Append the scraped link to the list

# Save the scraped data and links to a CSV file
filename_data = 'scraped_data.csv'
keys = scraped_data[0].keys() if scraped_data else []
with open(filename_data, 'w', newline='') as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    writer.writerows(scraped_data)

filename_links = 'scraped_links.csv'
with open(filename_links, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Scraped Links'])
    writer.writerows([[link] for link in scraped_links])

# Open a new browser page or perform any necessary operations
time.sleep(20)
driver.quit()
