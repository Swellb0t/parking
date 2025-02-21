from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Function to extract information from the page and save it to a text file
def extract_and_save_info(url, filename):
    # Set up the Chrome driver
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.binary_location = '/usr/bin/google-chrome'
    service = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Load the page
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load (adjust the timeout as needed)
        
        # Get the page source after JavaScript execution
        page_source = driver.page_source
        
        # Parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the ul element with class 'pplistview' and extract its contents
        pplistview = soup.find('ul', class_='pplistview')
        if pplistview:
            # Extract information from the list items
            info_list = [item.text.strip() for item in pplistview.find_all('li')]
            
            # Save the information to the file
            with open(filename, 'a', encoding='utf-8') as f:
                f.write('\n'.join(info_list))
                f.write('\n\n')
                
            print(f"Information extracted and saved to {filename}")
        else:
            print("No information found on the page.")
    except Exception as e:
        print("Error:", e)
    finally:
        # Quit the driver
        driver.quit()

# Base URL
base_url = 'https://portlandme.rmcpay.com/#results?violationid={}'
# Initial violation ID
initial_violation_id = 71126632

# Perform 5 iterations
for i in range(20):
    # Generate URL with incremented violation ID
    url = base_url.format(initial_violation_id + i)
    # Generate filename for each iteration
    filename = f'results_{initial_violation_id + i}.txt'
    # Extract and save information
    extract_and_save_info(url, filename)
