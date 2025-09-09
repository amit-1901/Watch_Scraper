# watch_scraper.py
#
# Objective: Scrape watch data from Flipkart, filter by price, and save to an Excel file.
# The script uses an Object-Oriented Programming (OOP) approach.
#
# Prerequisites:
# You need to install the following libraries before running this script:
# pip install selenium
# pip install beautifulsoup4
# pip install pandas
# pip install openpyxl
#
# You will also need to have a browser (like Chrome) and its corresponding WebDriver
# installed. The `webdriver_manager` library can handle this automatically for you.
# pip install webdriver-manager

import pandas as pd
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time


class WatchScraper:
    """
    A class to encapsulate the entire web scraping process for watches from Flipkart.
    It handles fetching, parsing, data extraction, filtering, and saving the results
    using a headless browser to bypass bot detection.
    """

    def __init__(self, base_url, price_limit=2000):
        """
        Initializes the scraper with a URL and a price limit.

        Args:
            base_url (str): The URL of the Flipkart search page.
            price_limit (int): The maximum price for watches to be included in the output.
        """
        self.base_url = base_url
        self.price_limit = price_limit
        self.product_data = []
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """
        Initializes and returns a Selenium WebDriver instance.
        Uses a headless browser and sets up options to mimic a real user.
        """
        try:
            options = Options()
            # options.add_argument("--headless")  # Run in headless mode (no visible browser UI)
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except WebDriverException as e:
            print(f"Error initializing WebDriver: {e}")
            print("Please ensure you have Chrome installed and a compatible WebDriver.")
            return None

    def fetch_page_source(self):
        """
        Navigates to the URL using the WebDriver and fetches the full page source.
        This handles JavaScript rendering and redirects.
        """
        if not self.driver:
            return None

        print(f"Navigating to {self.base_url} using Selenium...")
        try:
            self.driver.get(self.base_url)
            # Add a short delay to allow the page to fully load, including dynamic content.
            time.sleep(5)

            # Check for the reCAPTCHA page specifically.
            if "Are you a human?" in self.driver.page_source:
                print(
                    "CAPTCHA detected. Cannot proceed. Please run the script on a different network or try again later.")
                return None

            return self.driver.page_source
        except (WebDriverException, TimeoutException) as e:
            print(f"An error occurred while fetching the page with Selenium: {e}")
            return None
        finally:
            self.driver.quit()  # Always quit the driver to free up resources

    def _parse_price(self, price_str):
        """
        Helper method to parse and clean the price string into an integer.
        Handles various currency symbols and commas.
        """
        if not price_str:
            return None
        # Remove currency symbols (e.g., ₹), commas, and spaces
        cleaned_price = re.sub(r'[₹,]', '', price_str).strip()
        try:
            return int(cleaned_price)
        except (ValueError, TypeError):
            return None

    def extract_watch_data(self, html_content):
        """
        Parses the HTML content to extract watch information.

        Args:
            html_content (str): The HTML content of the page.
        """
        if not html_content:
            return

        print("Extracting watch data...")
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all containers for individual product cards
        # Flipkart's class names can change, so this might need updating.
        product_containers = soup.find_all('div', {'class': 'hCKiGj'})

        if not product_containers:
            print("No product containers found. The class names might have changed.")
            return

        for container in product_containers:
            try:
                # Find the element for the product name and brand
                brand_name = container.find('div', {'class': 'syl9yP'})
                name_element = container.find('a', {'class': 'WKTcLC'})

                watch_name = name_element.text.strip()
                brand = brand_name.text.strip()  # Assumes brand is the first word

                # Find the element for the price
                price_element = container.find('div', {'class': 'Nx9bqj'})
                if not price_element:
                    continue
                price = self._parse_price(price_element.text)

                # Find the availability status, if available
                availability = "In Stock"

                # Filter by price and add to the list
                if price and price <= self.price_limit:
                    self.product_data.append({
                        'Watch Name': watch_name,
                        'Brand': brand,
                        'Price': price,
                        'Availability': availability
                    })
            except Exception as e:
                print(f"Error extracting data for a product: {e}")
                continue

        print(f"Found {len(self.product_data)} watches under ₹{self.price_limit}.")

    def save_to_excel(self, filename="watch_data.xlsx"):
        """
        Saves the extracted watch data to an Excel file using pandas.

        Args:
            filename (str): The name of the Excel file to save the data.
        """
        if not self.product_data:
            print("No data to save. The scraped list is empty.")
            return

        try:
            df = pd.DataFrame(self.product_data)
            df.to_excel(filename, index=False)
            print(f"Successfully saved {len(self.product_data)} records to {filename}")
        except Exception as e:
            print(f"An error occurred while saving to Excel: {e}")

    def run_scraper(self):
        """
        Executes the full scraping process.
        """
        html_content = self.fetch_page_source()
        if html_content:
            self.extract_watch_data(html_content)
            self.save_to_excel()


if __name__ == "__main__":
    # URL for "Watches for Men under 2000" on Flipkart
    flipkart_url = "https://www.flipkart.com/search?q=watches+for+men+under+2000"

    # Create an instance of the scraper class
    scraper = WatchScraper(base_url=flipkart_url, price_limit=2000)

    # Run the scraping process
    scraper.run_scraper()
