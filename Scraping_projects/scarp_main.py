from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
import time

# Set up Selenium WebDriver
def setup_driver():
    # Set up Chrome options
    options = Options()
    #options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.binary_location = "/home/vignesh/Downloads/Chrome_Auto_Testing/chrome-linux64/chrome"  # Path to the Chrome executable

    # Path to the ChromeDriver executable
    driver_path = "/home/vignesh/Downloads/Chrome_Auto_Testing/chromedriver-linux64/chromedriver"
    service = Service(driver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Scrape the e-commerce test site
def scrape_webscraper_test_site(url):
    driver = setup_driver()
    url = "https://dhan.co/nifty-stocks-list/nifty-50/"
    driver.get(url)

    try:
        time.sleep(5)  # Wait for the page to load

        # Get the table
        table = driver.find_element(By.XPATH, '')
        print(table)
        # Get the table rows
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            # Get the row cells
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                print(cell.text)

    finally:
        # Close the browser
        driver.quit()

# Main function
if __name__ == "__main__":
    target_url = "https://webscraper.io/test-sites/e-commerce/allinone"  # Replace with your target website
    scrape_webscraper_test_site(target_url)
