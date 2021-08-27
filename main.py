url_form_google_spreadsheet = "https://docs.google.com/forms/d/e/1FAIpQLScToPKFEXmFbg5wyUk5ZmUF4LLt7hU4mzYhI4m5Yeq-V0mPZg/viewform?usp=sf_link"
zillow_url = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.70318068457031%2C%22east%22%3A-122.16347731542969%2C%22south%22%3A37.61593514575081%2C%22north%22%3A37.93430501246165%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
from bs4 import BeautifulSoup
import requests
import lxml
#requesting the data
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
accept_lang = "ru-UA,ru-RU;q=0.9,ru;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,uk;q=0.4"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": accept_lang
}
response = requests.get(zillow_url, headers=headers)
response.raise_for_status()
web_response = response.text
#finding the data we want to collect
soup = BeautifulSoup(web_response, "lxml")
#address data
address_list = []
addresses = soup.findAll(name="address", class_='list-card-addr')
for address in addresses:
    text_address = address.text
    address_list.append(text_address)
#price data
price_list = []
prices = soup.findAll(name="div", class_='list-card-price')
for price in prices:
    text_price = price.text
    price_list.append(text_price)
#link of each house data
link_list = []
links = soup.findAll(name="a", class_='list-card-link list-card-link-top-margin')
for url in links:
    if url.has_attr('href'):
        link = url.attrs['href']
        link_list.append(link)

# we need to enter the data using selenium
from selenium import webdriver
from time import sleep
chrome_web_driver = "C:\\Users\\Lenovo\\Desktop\\samourou python\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_web_driver)
driver.get(url_form_google_spreadsheet)
sleep(5)

# lets find the xpath of each input
#after we will use a loop to submit each request
for n in range(1, 10):
    address_xpath = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_xpath.send_keys(address_list[n-1])
    sleep(2)
    price_xpath = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_xpath.send_keys(price_list[n-1])
    sleep(2)
    link_xpath = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_xpath.send_keys(link_list[n-1])
    sleep(2)
    click_on_submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    click_on_submit.click()
    sleep(10)
    next = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next.click()
    sleep(10)


