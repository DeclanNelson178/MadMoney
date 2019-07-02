import bs4
import requests
url = 'https://www.thestreet.com/jim-cramer/rally-runs-low-on-fuel-cramers-mad-money-recap-june-11-14988480'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, 'lxml')
article = soup.text
tickers = []
magic_word = 'Yeti Holdings ('
location  = article.find(magic_word)
sentence = ''
for x in range(len(magic_word) * 2):
    sentence += article[location + x]

for words in sentence.split():
    if words.__contains__('('):
        print(words)
