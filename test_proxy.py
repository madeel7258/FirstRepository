from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

def check_proxies(csv_file):
    working_proxies = []

    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)
    options.add_argument('--disable-gpu')  # Disable GPU acceleration (may be required on some systems)
    driver = webdriver.Chrome(options=options)

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            ip = row[0]
            port = row[1]
            proxy = f"{ip}:{port}"

            try:
                # Configure Chrome to use the proxy
                options.add_argument(f'--proxy-server={proxy}')

                # Open a test URL using the proxy
                driver.get('https://www.daft.ie/')

                # Check if the page loaded successfully (you can customize this condition based on your requirements)
                if 'Example Domain' in driver.title:
                    working_proxies.append(proxy)

            except Exception:
                continue

    driver.quit()

    return working_proxies