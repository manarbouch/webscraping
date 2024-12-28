import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Path to ChromeDriver
service = Service('C:/Users/bouch/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')

# Set up browser options with a user-agent
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")

# Initialize the WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the website
    driver.get('https://www.yearupalumni.org/s/1841/interior.aspx?sid=1841&gid=2&pgid=440')

    # Wait for elements to load on the page
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'a'))  # Adjusted locator
    )

    # Scroll down to load more content (if applicable)
    for _ in range(3):  # Scroll 3 times
        driver.execute_script("window.scrollBy(0, 1000);")  # Scroll down
        time.sleep(2)  # Wait for the content to load

    # Fetch the page source after scrolling
    content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Initialize an empty list for results
    results = []

    # Scrape the desired elements
    for element in soup.findAll('a', href=True):  # Scrape all anchor tags
        # Extract the text from the <a> tag
        title = element.text.strip()

        # Append only non-empty titles to the results list
        if title:
            results.append({'title': title})

    # Print the scraped article titles
    print("Scraped Titles:")
    for i, result in enumerate(results, start=1):
        print(f"{i}. Title: {result['title']}")

    # Save results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv('titles.csv', index=False, encoding='utf-8')

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Prevent the browser from closing immediately
    input("Press Enter to exit and close the browser...")

    # Close the WebDriver
    driver.quit()
