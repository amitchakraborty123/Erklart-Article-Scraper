'''
Author: Amit Chakraborty
Project: Erklart Website Article Scraper
Profile URL: https://github.com/amitchakraborty123
E-mail: mr.amitc55@gmail.com
'''

import datetime
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

x = datetime.datetime.now()
n = x.strftime("__%b_%d_%Y")
url = input("Input Category URL: ")
folder_name = url.split('/')[-2]

def get_data():
    print('=================== Data Scraping ===================')
    """main url"""
    """set main page 0"""
    pag = 0
    while True:
        """Increase page 1 in every loop"""
        pag += 1
        print(">>>>>>>>>>>>>>>>>>> page: " + str(pag))
        """Getting the source of page """
        while True:
            try:
                soup = BeautifulSoup(requests.get(f'{url}page/{pag}/').content, 'lxml')
                temp = soup.find('header', {'class': 'entry-header'}).text.replace('\n', '')
                break
            except:
                input('Error occurs. Please check the error. And press enter:')

        try:
            """Find all article """
            divs = soup.find('div', {'id': 'primary'}).find_all('article', {'class': 'post'})
            """If article is 0 then finish the loop"""
            if len(divs) == 0:
                break
            """Get each article """
            for div in divs:
                title = ''
                link = ''
                description = ''
                category = ''
                """Get the title of article"""
                try:
                    title = div.find('header', {'class': 'entry-header'}).text.replace('\n', '')
                except:
                    pass
                """Get the link of article"""
                try:
                    link = div.find('header', {'class': 'entry-header'}).find('a')['href']
                except:
                    pass
                """Get the Description of article"""
                try:
                    des = div.find('div', {'class': 'entry-content'}).find_all('p')
                    description = '\n\n'.join(d.text for d in des)
                except:
                    pass
                """Get the category of article"""
                try:
                    category = div.find('footer', {'class': 'entry-footer'}).find('span', {'class': 'cat-links'}).text.replace('Categorized as', '')
                except:
                    pass
                """Make all data to json"""
                data = {
                    'Title': title,
                    'URL': link,
                    'Description': description,
                    'Category': category,
                }
                # print(data)
                """Add the json data to array"""
                df = pd.DataFrame([data])
                df.to_csv(f'{folder_name}/Data_{n}.csv', mode='a', header=not os.path.exists(f'{folder_name}/Data_{n}.csv'), encoding='utf-8-sig', index=False)
        except:
            pass


if __name__ == '__main__':
    """Make a folder for data save if folder is already create it pass"""
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        pass
    get_data()

