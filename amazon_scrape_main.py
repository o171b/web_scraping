import csv
from tarfile import RECORDSIZE
from webbrowser import Chrome
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_url(search_term):
    template = 'https://www.amazon.ae/s?k={}&crid=1O8RS7WWAKCH3&sprefix=ultrawide+monito%2Caps%2C216&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page{}'
    return template.format(search_term)

    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.ae' + atag.get('href')
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span' , 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = '' 
        review_count = '' 

    result = (description, price, rating, review_count,url)
    return result


def main(search_term):
    """run main program routine"""
    #start web driver
    chrome_options = Options()
    chrome_options.use_chromium = True
    driver = webdriver.Chrome(options=chrome_options)

    records = []
    url = get_url(search_term)

    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()


    with open('results.csv','w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'url'])
        writer.writerows(records)

main('samsung galaxy s22')