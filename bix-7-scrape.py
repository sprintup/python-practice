from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import csv
import time

# Setup Firefox options
options = Options()
options.add_argument("--headless")  # Run in background

# Path to your GeckoDriver
service = Service("C:\Program Files\Mozilla Firefox\geckodriver.exe")  # Replace with actual path

driver = webdriver.Firefox(service=service, options=options)

# CSV setup
with open("bix7_2025_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age", "Bib", "Location", "Pace", "Finish Time"])

    # Loop through all pages
    for page_num in range(1, 160):
        print(f"Scraping page {page_num}...")
        url = f"https://www.athlinks.com/event/180346/results/Event/1115843/Course/2615405/Results?page={page_num}"
        driver.get(url)
        time.sleep(2)  # Wait for JS to load

        results = driver.find_elements(By.CLASS_NAME, "link-to-irp")
        for result in results:
            try:
                name = result.find_element(By.CLASS_NAME, "athName-display").text
                age = result.find_elements(By.CLASS_NAME, "MuiTypography-body1")[0].text
                bib = result.find_elements(By.CLASS_NAME, "MuiTypography-body1")[1].text
                location = result.find_element(By.ID, "location").text
                pace = result.find_elements(By.CLASS_NAME, "col")[3].text.split("\n")[0]
                finish_time = result.find_element(By.CLASS_NAME, "col-2").text.split("\n")[0]

                writer.writerow([name, age, bib, location, pace, finish_time])
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                continue

driver.quit()
print("Scraping complete.")
