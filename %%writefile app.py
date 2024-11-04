%%writefile app.py

# Step 3: Import Necessary Libraries and Initialize Chrome Driver
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import csv
import pandas as pd
from tqdm import tqdm  # For progress bars
import streamlit as st

# Install the ChromeDriver version that matches the installed Chrome version
chromedriver_autoinstaller.install()

class YellowPageScraper:
    BASE_URL = 'https://www.yellowpages.com'

    def __init__(self, search_terms, geo_location_terms, start_page, max_pages, file_path='/content/sample_data/yellow_page/business_listings.csv'):
        self.search_terms = search_terms
        self.geo_location_terms = geo_location_terms
        self.current_page = start_page
        self.max_pages = max_pages
        self.file_path = file_path

        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Setup headless Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--window-size=1920x1080")  # Set a standard window size

        # Create a new instance of the Chrome driver
        self.driver = webdriver.Chrome(options=chrome_options)

    def extract_business_listing(self, card):
        """Extract business information from a card element."""
        rank = card.find_element("css selector", ".info-primary h2").text.strip() if card.find_elements("css selector", ".info-primary h2") else ''
        business_name = card.find_element("css selector", ".business-name span").text.strip() if card.find_elements("css selector", ".business-name span") else ''
        phone_number = card.find_element("css selector", ".phones").text.strip() if card.find_elements("css selector", ".phones") else ''
        business_page = card.find_element("css selector", ".business-name").get_attribute('href') if card.find_elements("css selector", ".business-name") else ''
        website = card.find_element("css selector", ".track-visit-website").get_attribute('href') if card.find_elements("css selector", ".track-visit-website") else ''
        category = ', '.join([a.text.strip() for a in card.find_elements("css selector", ".categories a")]) if card.find_elements("css selector", ".categories a") else ''
        rating = card.find_element("css selector", ".ratings .count").text.strip('()') if card.find_elements("css selector", ".ratings .count") else ''
        street_name = card.find_element("css selector", ".street-address").text.strip() if card.find_elements("css selector", ".street-address") else ''
        locality = card.find_element("css selector", ".locality").text.strip() if card.find_elements("css selector", ".locality") else ''

        # Split locality into components
        if locality:
            locality_parts = locality.split(",")
            if len(locality_parts) == 2:
                region = locality_parts[1].strip()
                locality = locality_parts[0].strip()
            else:
                locality = locality_parts[0].strip()
                region = ''
        else:
            locality, region = '', ''

        return {
            "Rank": rank,
            "Business Name": business_name,
            "Phone Number": phone_number,
            "Business Page": business_page,
            "Website": website,
            "Category": category,
            "Rating": rating,
            "Street Name": street_name,
            "Locality": locality,
            "Region": region
        }

    def save_to_csv(self, data_list):
        """Save the extracted data to a CSV file."""
        fieldnames = ["Rank", "Business Name", "Phone Number", "Business Page", "Website", "Category", "Rating", "Street Name", "Locality", "Region"]

        with open(self.file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Check if file is empty
                writer.writeheader()
            writer.writerows(data_list)

    def scrape(self):
        """Main scraping function with a maximum page limit."""
        results = []
        while self.current_page <= self.max_pages:
            url = f"{self.BASE_URL}/search?search_terms={self.search_terms}&geo_location_terms={self.geo_location_terms}&page={self.current_page}"
            try:
                self.driver.get(url)
                time.sleep(3)  # Adjust this as necessary

                # Find all business cards
                cards = self.driver.find_elements("css selector", ".organic .srp-listing")
                if not cards:
                    print(f"No more cards found on page {self.current_page}. Stopping.")
                    break  # No more cards to scrape

                for card in tqdm(cards, desc=f"Scraping Listings (Page {self.current_page}):", leave=False):  # Add progress bar
                    business_info = self.extract_business_listing(card)
                    results.append(business_info)

                self.current_page += 1  # Move to the next page

            except Exception as e:
                print(f"An error occurred on page {self.current_page}: {e}")
                break  # Exit on error to avoid an infinite loop

        # Save all results to CSV
        self.save_to_csv(results)

        # Close the driver
        self.driver.quit()

# Streamlit application
def main():
    st.title("Yellow Pages Scraper")
    search_terms = st.text_input("Search Terms:", "carpet")
    geo_location_terms = st.text_input("Geo Location Terms:", "Boston")
    start_page = st.number_input("Start Page:", min_value=1, value=1)
    max_pages = st.number_input("Max Pages to Scrape:", min_value=1, value=2)

    if st.button("Start Scraping"):
        if not search_terms or not geo_location_terms:
            st.error("Please enter both search terms and location.")
        else:
            output_file_path = '/content/sample_data/yellow_page/business_listings.csv'
            scraper = YellowPageScraper(search_terms, geo_location_terms, start_page, max_pages, file_path=output_file_path)

            # Progress bar
            progress_bar = st.progress(0)

            # Scrape the data
            scraper.scrape()

            # Indicate completion
            st.success("Scraping completed! Checking for CSV file...")

            # Check if the CSV file exists
            if os.path.exists(output_file_path):
                with open(output_file_path, 'rb') as file:
                    st.download_button(
                        label="Download CSV file here",
                        data=file,
                        file_name="business_listings.csv",
                        mime="text/csv"
                    )
            else:
                st.error("CSV file not found!")

if __name__ == "__main__":
    main()
