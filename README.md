# Watch_Scraper

## Project Description

This is a Python-based automation project that scrapes **watch data from Flipkart**, filters results by price (default: under ₹2000), and saves them into an **Excel file**.  
The project demonstrates the use of **Object-Oriented Programming (OOP)** concepts along with modern scraping tools like **Selenium** and **BeautifulSoup**.

## Features

- **Automated Data Fetching:** Scrapes product details (watch name, brand, price, availability) from Flipkart.  
- **Price Filtering:** Automatically filters results under a configurable price limit.  
- **Data Export:** Saves the final dataset to an Excel file (`watch_data.xlsx`).  
- **Headless Browser:** Uses Selenium WebDriver with headless mode to handle dynamic content.  
- **Error Handling:** Gracefully manages bot detection, timeouts, and parsing issues.  

## Technology Stack

- **Language:** Python (3.8+)  
- **Libraries:** Selenium, BeautifulSoup4, Pandas, OpenPyXL, Webdriver-Manager  
- **Browser:** Chrome / Chromium  

## Getting Started

### 1. Prerequisites

- Python 3.8 or higher  
- Google Chrome or Chromium installed  
- `pip` (Python package manager)  

### 2. Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/Watch_Scraper.git
    cd Watch_Scraper
    ```

2. **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, run:)*  
    ```bash
    pip install selenium beautifulsoup4 pandas openpyxl webdriver-manager
    ```

### 3. Running the Application

Run the scraper script:
```bash
python watch_scraper.py
