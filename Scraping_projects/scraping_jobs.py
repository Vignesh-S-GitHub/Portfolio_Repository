from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


# Set up Selenium WebDriver
def setup_driver():
    # Set up Chrome options
    options = Options()
    #options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-cache")
    options.add_argument("--disable-application-cache")
    options.add_argument("--start-maximized")
    options.binary_location = "/home/vignesh/Chrome_Auto_Testing/chrome-linux64/chrome"
    driver_path = "/home/vignesh/Chrome_Auto_Testing/chromedriver-linux64/chromedriver"
    service = Service(driver_path)

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Open the Naukri URL
def scrape_webscraper_test_site(url):
    driver = setup_driver()
    driver.get(url)

    try:
        time.sleep(5)  # Wait for the page to load
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper"))
        )
        html_load = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
        
        for each in html_load:
            row1_class = each.find_elements(By.CLASS_NAME, "row1")
            for row1 in row1_class:
                title = row1.find_element(By.CSS_SELECTOR, "a.title")
                print(f"Job Title: {title.text}")
            
            row2_class = each.find_elements(By.CLASS_NAME, "row2")
            for row2 in row2_class:
                company = row2.find_element(By.CLASS_NAME, "comp-dtls-wrap")
                try:
                    # Locate the title element
                    title_element = company.find_element(By.CSS_SELECTOR, "a.comp-name.mw-25")
                    title = title_element.get_attribute("title")  # Get the title attribute
                    print(f"Company Title: {title}")
                except NoSuchElementException:
                    print("No title found")

                try:
                    # Locate the rating element
                    rating_element = company.find_element(By.CSS_SELECTOR, "span.main-2")
                    rating = rating_element.text  # Get the inner text
                    print(f"Company Rating: {rating}")
                except NoSuchElementException:
                    print("No rating found")

    finally:
        # Close the browser
        driver.quit()

# # Save data to CSV
# df = pd.DataFrame(jobs)
# df.to_csv("naukri_jobs.csv", index=False)

if __name__ == "__main__":
    target_url = "https://www.naukri.com/data-engineer-jobs?k=%22data%20engineer%22&experience=3&cityTypeGid=97&cityTypeGid=183&ugTypeGid=12&jobAge=7"
    scrape_webscraper_test_site(target_url)
