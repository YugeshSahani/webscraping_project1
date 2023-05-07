import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}


product = input('Search for products, brands and more: ')

search_query = product.replace(' ', '+')   
base_url = f'https://www.flipkart.com/search?q={search_query}'

response_page = requests.get(base_url, headers=headers)
soup_page = BeautifulSoup(response_page.content, 'html.parser')

total_page = soup_page.find('div', attrs={'class': '_2MImiq'})
total_page = total_page.find('span').text.split(' ')[-1]

while True:
    last_page = input(f'Max page is {total_page}.\nEnter no. of page: ')
    last_page = int(last_page)
    if last_page >= int(total_page) or last_page is not int:
        print('Invalid input')
        break
    else:
        pass
items = []
for i in range(1, (last_page)+1):
    print(f'Processing {i}...'+base_url + f'&page={i}')
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)  #headers = headers to act as human
    soup = BeautifulSoup(response.content, 'html.parser')
    
    results = soup.find_all('div', attrs={'class': '_1AtVbE col-12-12'})

    for result in results:
        product_name = result.find('div', {'class': '_4rR01T'})
        if product_name is not None:
            product_name = product_name.text
        
        else:
            continue
        
        try:
            rating = result.find('div', attrs={'class': '_3LWZlK'}).text
            ratings_and_reviews = result.find_all('span', attrs={'class':'_2_R_DZ'})[0].text 
            ratings_and_reviews_list  = ratings_and_reviews.split(' ')  # .split(' ') to make list from text
            rating_count = ratings_and_reviews_list[0]

        except AttributeError:
            continue

        try:
            price = result.find('div', {'class': '_30jeq3 _1_WHN1'}).text
            product_url = 'https://www.flipkart.com' + result.div.a['href'] 
            # print(rating_count, product_url)
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    sleep(2.5)
    
df = pd.DataFrame(items, columns=['product name', 'rating', 'rating count','price', 'product url'])
print(df)
df.to_excel(f'{search_query}.xlsx')


        