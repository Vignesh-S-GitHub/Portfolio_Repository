from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for some environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues

service = Service("/path/to/chromedriver", port=9515)  # Replace with your actual path
driver = webdriver.Chrome(service=service, options=chrome_options)

# Example usage
driver.get("https://the-internet.herokuapp.com/")
print("Page title:", driver.title)

driver.quit()
