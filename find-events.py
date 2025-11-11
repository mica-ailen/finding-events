from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

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
    
    time.sleep(2) 

    load_more_clicked = 0
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='sc-bb566763-63 YvgGs']"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            time.sleep(1)
            
            load_more_button.click()
            load_more_clicked += 1
            print(f"Clicked 'Load More' button {load_more_clicked} times")
            
            time.sleep(3) 
            
        except (TimeoutException, NoSuchElementException) as e:
            print("No more 'Load More' button found or all events loaded!")
            break
    
    print("\nExtracting all events...")
    event_items = driver.find_elements(By.XPATH, "//div[@class='sc-bb566763-28 gEMIVp xs-12 md-4']")
    print(f"Total event items found: {len(event_items)}")
    
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