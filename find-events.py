from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

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
    
    events_skipped = 0
    
    for i, event_item in enumerate(event_items, 1):
        try:
            date_elements = event_item.find_elements(By.XPATH, ".//div[@class='sc-2a579a92-26 EPKGt']")
            
            if len(date_elements) == 0:
                events_skipped += 1
                print(f"Event {i}: Skipped (no dates)")
                continue
            
        
            name = event_item.find_element(By.XPATH, ".//h3[@class='sc-2a579a92-24 bZVIvy']").text
            dates = date_elements[0].text
            event_url = event_item.find_element(By.XPATH, ".//a[@class='link-internal']").get_attribute('href')
            
            event_data = {
                'name': name,
                'dates': dates,
                'url': event_url
            }
            events.append(event_data)
            
            print(f"\nEvent {i}:")
            print(f"Name: {name}")
            print(f"Dates: {dates}")
            print(f"Link: {event_url}")
            
        except Exception as e:
            print(f"Error extracting event {i}: {e}")
            events_skipped += 1
            continue
    
    print(f"Total items processed: {len(event_items)}")
    
except Exception as e:
    print(f"Error: {e}")
    
finally:
    driver.quit()

with open('copenhagen_events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)
print("\nEvents saved to copenhagen_events.json")