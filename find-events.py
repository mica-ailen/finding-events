from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL to scrape
url = "https://www.visitcopenhagen.com/explore/events-cid58/events-cid59?filters=region:2"

driver = webdriver.Chrome()
events = []

try:
    driver.get(url)
    
    element = WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.ID, "declineButton"))
    )
    element.click()  
    print("Cookie declined!")

    driver.implicitly_wait(10)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    event_items = driver.find_elements(By.XPATH, "//div[@class='sc-bb566763-28 gEMIVp xs-12 md-4']")
    print(len(event_items))

    for event_item in event_items:
        name = event_item.find_element(By.XPATH, ".//h3[@class='sc-2a579a92-24 bZVIvy']").text
        dates = event_item.find_element(By.XPATH,".//div[@class='sc-2a579a92-26 EPKGt']").text
        url = event_item.find_element(By.XPATH, ".//a[@class='link-internal']").get_attribute('href')

        print(f"Name: {name}")
        print(f"Dates: {dates}")
        print(f"Link: {url}")
    
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    driver.quit()