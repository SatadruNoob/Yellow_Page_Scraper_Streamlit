                                                                 
  **Yellow_Page_Scraper_Streamlit_Selenium_Beautifulsoup**

# Table of Contents

1.[Overview](#overview)  
2.[Features](#features)  
3.[Installation](#installation)  
  - [Clone the Repository](#clone-the-repository)  
  - [Set Up the Environment](#set-up-the-environment)  
    - [Create a Virtual Environment](#create-a-virtual-environment)  
    - [Activate the Virtual Environment](#activate-the-virtual-environment)  
    - [Install Required Packages](#install-required-packages)  
    - [Install ChromeDriver](#install-chromedriver)  
    [Configuration](#configuration)  
    [Requirements](#requirements)  
4.[Usage](#usage)  
  - [Start the Application](#start-the-application)  
5.[Code Structure](#code-structure)  
6.[API Reference](#api-reference)  
7.[Troubleshooting](#troubleshooting)  
8.[Contributing](#contributing)  
9.[License](#license)  
10.[Acknowledgements](#acknowledgements)



![one click yellow gig photo](https://github.com/user-attachments/assets/aa7e785a-3d08-49b6-b5b3-39e39b6ac77d)


![Yellow page scraper fiverr gig front](https://github.com/user-attachments/assets/69978b01-689c-48af-b2b9-37b22af1f50e)


https://github.com/user-attachments/assets/e092d441-a8d5-435a-a433-05920e3ce45e




# 1. Overview
- The Yellow Pages Business Scraper is a Python application built specifically for use in Google Colab. 
- This application allows users to gather business information, such as business name, phone number, address, and website, directly from Yellow Pages. 
- It utilizes Selenium for web scraping, Streamlit for the web interface, and localtunnel to enable public access to the Streamlit application within the Colab environment.


# 2. Features
- Search by Keywords and Location: Input search terms and geographic location to filter results.
- Scrapes Business Details: Extracts business name, phone number, address, and website from Yellow Pages.
- CSV Export: Download scraped data as a CSV file for easy data management.


# 3. Installation
##  Clone the Repository
First, clone the repository to access the application files:

```bash
    Copy code
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
```


# 4. Set Up the Environment
Since this scraper runs in Google Colab, the following steps are tailored to work within Colab’s environment.




### Configuration

####  Libraries Installed in Colab:
```bash
streamlit==1.25.0
selenium==4.12.0
tqdm==4.66.1
pandas==2.1.1
chromedriver-autoinstaller==0.6.2
```


### Usage

####  Start the Application


  
1. Step 1 of Application:
First install the required libraries as shown below. This is important and should not be merged or put in the same code block with step 2

```
# Step 1: Install Required Packages
# Update the package list and install wget and unzip
!apt-get update -qq
!apt-get install -y wget unzip

# Install necessary Python packages
!pip install tqdm
!pip install chromedriver-autoinstaller
!pip install selenium
!pip install pandas  # Ensure pandas is installed for data handling
!pip install streamlit -q  # Install Streamlit

# Step 2: Download and Install Google Chrome
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -q
!dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y install -f
!rm google-chrome-stable_current_amd64.deb  # Clean up the downloaded file

```


2. Step 2 of Application:
Set up the scraper code: Copy and save the following code into a file named app.py in the Colab environment.

  ```bash
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
                time.sleep(5)  # Adjust this as necessary
                
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
```

    


3. Step 3 of Application:
Run Streamlit with Localtunnel: Start the Streamlit app and expose it using localtunnel.
   
```bash
# Install necessary packages and set up the environment
!pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com

# Install localtunnel globally to avoid confirmation prompts
!npm install -g localtunnel

import subprocess
import re
from IPython.display import display, HTML

# Start Streamlit app and use localtunnel, capturing the output
streamlit_process = subprocess.Popen(['streamlit', 'run', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
localtunnel_process = subprocess.Popen(['lt', '--port', '8501'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to extract the URL from localtunnel output
def get_localtunnel_url():
    while True:
        output = localtunnel_process.stdout.readline().decode('utf-8')
        if output.startswith('your url is:'):
            url = output.split('your url is: ')[-1].strip()
            return url

# Wait for the localtunnel URL to be available
external_url = get_localtunnel_url()

# Display the URL as a clickable link in the notebook
display(HTML(f'<a href="{external_url}" target="_blank">Click here to open your Streamlit app!</a>'))
```
     
4. Step 5 of Application
A url is auto-generated after step 3 in the Colab environment. Click on the generated link. This opens the NGROK gateway that establishes the secure connection between Colab Engine and the external url. Type in the IP address in the opened url obtained from step3. A new page opens showing the streamlit app. Now just input your desired search parameters, geo location, start page to scrape and maximum page to scrape and hit the Scrape button. The scarped data will be made available once when the scraping is completed, ready for downloading from the streamlit app itself.


# 5. Code Structure
1.app.py: Main application file containing the Streamlit interface and scraping logic.

2.scraped_data.csv: CSV file generated after scraping, available for download.


# 6. API Reference
This application operates through a Streamlit interface, so it does not use REST API endpoints. 

Inputs are handled through Streamlit form fields, and results are displayed directly in the Colab-hosted Streamlit app.


# 7. Troubleshooting
Errors with Chrome: Ensure Google Chrome is compatible with the version of ChromeDriver installed by chromedriver-autoinstaller.

Timeout Errors: Increase time.sleep() in the script to allow longer load times for each page.

Running streamlit is problematic in Colab so follow the instruction as described here exactly.

Colab-specific Issues: Re-run all cells if the Colab session disconnects due to inactivity.


# 8. Contributing
Contributions are welcome! Please submit issues or pull requests for bug fixes or improvements.


# 9. License
This project is licensed under the MIT License. See the LICENSE file for more information.


# 10. Acknowledgements

- Selenium Documentation
- Streamlit Documentation
- Localtunnel for URL tunneling
- Yellow Pages
