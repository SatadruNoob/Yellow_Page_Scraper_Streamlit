  # Yellow_Page_Scraper_Streamlit

# Table of Contents

[Overview](#overview)  
[Features](#features)  
[Installation](#installation)  
  - [Clone the Repository](#clone-the-repository)  
  - [Set Up the Environment](#set-up-the-environment)  
    - [Create a Virtual Environment](#create-a-virtual-environment)  
    - [Activate the Virtual Environment](#activate-the-virtual-environment)  
    - [Install Required Packages](#install-required-packages)  
    - [Install ChromeDriver](#install-chromedriver)  
[Configuration](#configuration)  
    - [Requirements](#requirements)  
[Usage](#usage)  
  - [Start the Application](#start-the-application)  
[Code Structure](#code-structure)  
[API Reference](#api-reference)  
[Troubleshooting](#troubleshooting)  
[Contributing](#contributing)  
[License](#license)  
[Acknowledgements](#acknowledgements)



# Overview
The Yellow Pages Business Scraper is a Python application built specifically for use in Google Colab. 
This application allows users to gather business information, such as business name, phone number, address, and website, directly from Yellow Pages. 
It utilizes Selenium for web scraping, Streamlit for the web interface, and localtunnel to enable public access to the Streamlit application within the Colab environment.


# Features
Search by Keywords and Location: Input search terms and geographic location to filter results.
Scrapes Business Details: Extracts business name, phone number, address, and website from Yellow Pages.
CSV Export: Download scraped data as a CSV file for easy data management.


# Installation
##  Clone the Repository
First, clone the repository to access the application files:

    ```bash
    Copy code
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```


# Set Up the Environment
Since this scraper runs in Google Colab, the following steps are tailored to work within Colab’s environment.

##  Create a Virtual Environment
To maintain dependency isolation, create a virtual environment:

    ```bash
    Copy code
    python -m venv venv
    ```

## Activate the Virtual Environment
Depending on your OS, activate the virtual environment:

    ```bash
    Copy code
    Windows
    venv\Scripts\activate
    ```

    ```macOS/Linux
    source venv/bin/activate
    ```

##  Install Required Packages
Install all necessary packages, including Selenium, Streamlit, chromedriver-autoinstaller, and localtunnel.

    ```bash
    Copy code
    !pip install -r requirements.txt
    ```
    
Note: Within Google Colab, these packages will be installed globally due to Colab’s setup.

##  Install ChromeDriver
Install ChromeDriver using chromedriver-autoinstaller, which handles version compatibility automatically:

    ```python
    Copy code
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()
    ```


# Configuration

##  Requirements
```
Python 3.x
Google Chrome (ensure compatibility with chromedriver-autoinstaller)
Selenium
Streamlit
Localtunnel for URL tunneling in Google Colab
```


# Usage

##  Start the Application
1.Set up the scraper code: Copy and save the following code into a file named app.py in the Colab environment.

  ```
    import streamlit as st
    import pandas as pd
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    import chromedriver_autoinstaller

    # Streamlit interface
    st.title("Yellow Pages Business Scraper (Colab)")
    
    search_term = st.text_input("Search Term", "e.g., plumber")
    location = st.text_input("Location", "e.g., Los Angeles")
    start_page = st.number_input("Start Page", min_value=1, max_value=100, value=1)
    max_pages = st.number_input("Max Pages to Scrape", min_value=1, max_value=100, value=1)
    
    if st.button("Start Scraping"):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)

        data = []
        url_template = "https://www.yellowpages.com/search?search_terms={}&geo_location_terms={}&page={}"
    
        # Scrape
        for page in range(start_page, start_page + max_pages):
            driver.get(url_template.format(search_term, location, page))
            time.sleep(2)
    
            listings = driver.find_elements(By.CLASS_NAME, "result")
            for listing in listings:
                name = listing.find_element(By.CLASS_NAME, "business-name").text
                phone = listing.find_element(By.CLASS_NAME, "phones").text
                address = listing.find_element(By.CLASS_NAME, "street-address").text
                website = listing.find_element(By.CLASS_NAME, "links").text
                data.append({"Name": name, "Phone": phone, "Address": address, "Website": website})
    
        driver.quit()
        df = pd.DataFrame(data)
        st.write(df)
        st.download_button("Download CSV", data=open("scraped_data.csv", "rb").read(), file_name="scraped_data.csv")
```

    


2. Run Streamlit with Localtunnel: Start the Streamlit app and expose it using localtunnel.
   
       ```import subprocess
       from IPython.display import display, HTML
        
       streamlit_process = subprocess.Popen(['streamlit', 'run', 'app.py', '--server.port', '8501'])
       localtunnel_process = subprocess.Popen(['lt', '--port', '8501'], stdout=subprocess.PIPE)
        
       for line in iter(localtunnel_process.stdout.readline, b''):
           if b'https://' in line:
               external_url = line.decode('utf-8').strip()
               display(HTML(f'<a href="{external_url}" target="_blank">Open Streamlit app</a>'))
               break
   ```
     
4. Open the Streamlit Interface:

   Click on the generated link to access the app and input your desired search parameters.


# Code Structure
1.app.py: Main application file containing the Streamlit interface and scraping logic.
2.scraped_data.csv: CSV file generated after scraping, available for download.


# API Reference
This application operates through a Streamlit interface, so it does not use REST API endpoints. 
Inputs are handled through Streamlit form fields, and results are displayed directly in the Colab-hosted Streamlit app.


# Troubleshooting
Errors with Chrome: Ensure Google Chrome is compatible with the version of ChromeDriver installed by chromedriver-autoinstaller.
Timeout Errors: Increase time.sleep() in the script to allow longer load times for each page.
Colab-specific Issues: Re-run all cells if the Colab session disconnects due to inactivity.


# Contributing
Contributions are welcome! Please submit issues or pull requests for bug fixes or improvements.


# License
This project is licensed under the MIT License. See the LICENSE file for more information.


# Acknowledgements

Selenium Documentation
Streamlit Documentation
Localtunnel for URL tunneling
Yellow Pages
