from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL to scrape
url = "https://www.visitcopenhagen.com/explore/events-cid58/events-cid59?filters=region:2;date-range:[2025-10-30T00:00:00.000Z%20TO%202025-12-31T23:59:59.999Z]"

driver = webdriver.Chrome()

try:
    driver.get(url)
    
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "declineButton"))
    )
    element.click()  
    print("Cookie declined!")
    
    title = driver.find_element(By.CLASS_NAME, "name")
    print(title.text)
    
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    driver.quit()