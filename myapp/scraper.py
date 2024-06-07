# api/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class CoinMarketCapScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    def scrape_coin(self, coin):
        print("scraper  called",coin.lower())
        url = f"https://coinmarketcap.com/currencies/{coin.lower()}/"
        self.driver.get(url)
        time.sleep(1)

        data = {}

        try:
            print("collecting data")
            data['price'] = self.driver.find_element(By.CSS_SELECTOR, '.priceValue___11gHJ').text
            data['price_change'] = self.driver.find_element(By.CSS_SELECTOR, '.sc-15yy2pl-0.feeyND').text
            data['market_cap'] = self.driver.find_element(By.CSS_SELECTOR, 'div.statsValue___2iaoZ').text
            data['market_cap_rank'] = self.driver.find_element(By.CSS_SELECTOR, 'div.namePill___3p_Ii.rank').text
            data['volume'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]/span').text
            data['volume_change'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[2]/span').text
            data['circulating_supply'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div').text
            data['total_supply'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div').text
            data['diluted_market_cap'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/div/div[1]/div[2]/div').text

            contracts = self.driver.find_elements(By.CSS_SELECTOR, 'div.contractAddress___3MNC_ a')
            data['contracts'] = [{'name': c.get_attribute('data-original-title'), 'address': c.text} for c in contracts]

            links = self.driver.find_elements(By.CSS_SELECTOR, 'ul.content___mN_4o li a')
            data['official_links'] = [{'name': l.get_attribute('data-original-title'), 'link': l.get_attribute('href')} for l in links]

            socials = self.driver.find_elements(By.CSS_SELECTOR, 'ul.list-unstyled li a')
            data['socials'] = [{'name': s.get_attribute('data-original-title'), 'url': s.get_attribute('href')} for s in socials]
            
        except Exception as e:
            print(f"Error fetching data for {coin_acronym}: {e}")

        return data
    

    def close(self):
        self.driver.quit()
