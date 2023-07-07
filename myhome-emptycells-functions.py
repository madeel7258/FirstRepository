import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def accept_cookies(driver):
    try:
        cookies_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
        cookies_option.click()
    except:
        pass

def retrieve_agent_name(driver):
    try:
        agent_name_xpath = ".//div[@class='group-card__details d-flex flex-column group-card__details--blue ng-star-inserted']"
        agent_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, agent_name_xpath)))
        #agent_element = driver.find_element((By.XPATH, agent_name_xpath))
        agent_name = agent_element.get_attribute("textContent")
        if agent_name:
            agent_name = agent_name.strip()
            return agent_name
    except:
        pass

    try:
        agent_name_xpath = ".//a[@class='group-card__details d-flex flex-column group-card__Details--blue ng-star-inserted']"
        agent_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, agent_name_xpath)))
        #agent_element = driver.find_element(By.XPATH, agent_name_xpath)
        agent_name = agent_element.get_attribute("textContent")
        if agent_name:
            agent_name = agent_name.strip()
            return agent_name
    except:
        pass

    return None

def retrieve_price(driver):
    try:
        price_element = driver.find_element(By.XPATH, '//b[@class="brochure__price p-1"]')
        price_value = price_element.get_attribute("textContent")
        if price_value:
            price_value = price_value.strip()
            return price_value
    except NoSuchElementException:
        pass

    return None

def scrape_data(df, driver):
    try:
        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            link = row['link']
            agent = row['agent']
            price = row['price']   

            if pd.isnull(agent) or pd.isnull(price):
                try:
                    # Open the link using Selenium
                    driver.get(link)
                    # Retrieve the agent name from the web page if it's missing
                    if pd.isnull(agent):
                        agent_name = retrieve_agent_name(driver)
                        if agent_name:
                            print(f"Retrieved agent name: {agent_name}")
                            agent = agent_name
                        else:
                            print(f"No agent name found for link '{link}'")

                    # Retrieve the price from the web page if it's missing
                    if pd.isnull(price):
                        price_value = retrieve_price(driver)
                        if price_value:
                            print(f"Retrieved price: {price_value}")
                            price = price_value
                        else:
                            print(f"No price found for link '{link}'")

                    # Update the DataFrame with the retrieved values
                    df.at[index, 'agent'] = agent
                    df.at[index, 'price'] = price

                except Exception as e:
                    print(f"An exception occurred for link '{link}': {str(e)}")
                    # Set agent and price as None to indicate failure
                    agent = None
                    price = None

        # Save the updated DataFrame to the CSV file
        df.to_csv('myhome_web_scrape_final.csv', index=False)

    except Exception as e:
        print(f"An exception occurred during scraping: {str(e)}")

    finally:
        # Close the browser
        driver.quit()
        return


def main():
    # Read the CSV file
    df = pd.read_csv('myhome_web_scrape_final.csv')
    # Handle cookie dialogue button
    url='https://www.myhome.ie/residential/ireland/property-for-sale'
    # Open the browser
    driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser
    driver.get(url)
    accept_cookies(driver)
    # Scrape data
    scrape_data(df, driver)
    return
if __name__ == "__main__":
    main()
