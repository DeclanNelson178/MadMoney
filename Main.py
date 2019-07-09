# API KEY: 86UKVGO0J2S8VMBN
from alpha_vantage.timeseries import TimeSeries
import requests
import pandas as pd
import bs4
import datetime
import time

# class which takes a mad money suggested article and finds tickers of the recommended stocks
class MadMoney:

    def __init__(self, url):
        self.url = url
        self.names = self.set_names(url)
        self.tickers = self.set_tickers(url)

    def get_names(self):
        return self.names

    def get_tickers(self):
        return self.tickers

    def set_tickers(self, url):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        article = soup.text
        tickers = ['tickers']
        for y in range(len(self.names)):
            magic_word = self.names[y] + ' ('
            location = article.find(magic_word)
            sentence = ''
            for x in range(len(magic_word) * 2):
                sentence += article[location + x]

            for words in sentence.split():
                if words.__contains__('('):
                    tickers.append(words)
        tickers.remove('tickers')
        for z in range(len(tickers)):
            holder = tickers[z]
            holder = holder[1:]  # for some reason was originally to -1 but got rid of that and it worked
            tickers[z] = holder
        return tickers

    def set_names(self, url):
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        article = soup.get_text()
        return self.snip_snip(article)


    def snip_snip(self, article):
        hit = False
        sentence = ''
        for word in article.split():
            if(word == 'Lightning' or hit == True):
                hit = True
                if (word == '.'):
                    break
                sentence += word + ' '
        hit_on = False
        suggest = ''
        for word in sentence.split():

            if hit_on == True:
                suggest += word + ' '

            if word == 'on':
                hit_on = True

        suggest = suggest.split(',')

        last_entry = suggest[-1]

        last_entry = last_entry.split('and')

        suggest.pop()
        suggest.append(last_entry[0])
        suggest.append(last_entry[1])

        for word in range(len(suggest)):
            if word == 0:
                suggest[word] = suggest[word][0:-1]
            else:
                suggest[word] = suggest[word][1:-1]

        return suggest

# alpha vantage API to get closing price given a ticker
def get_price(ticker):
    ts = TimeSeries(key='86UKVGO0J2S8VMBN', output_format='pandas')
    ticker = str(ticker)
    data, meta_data = ts.get_daily(symbol=ticker, outputsize='compact')
    close_price =  data['4. close'][-2]
    fname = ticker + '.txt'
    F = open(fname, 'a+')
    # if not check_duplicates(fname):
    F.write(str(close_price))
    F.write('\n')
    F.close()


# create file with the data opened for a stock
def create_db(fname):
    file = open(fname, 'a')
    if not check_duplicates(fname):
        date = str(datetime.datetime.now())[0:10]
        file.write(date)
        file.write('\n')
        file.close()


# check for duplicates
def check_duplicates(fname):
    F = open(fname, 'r')
    date = str(datetime.datetime.now())[0:10]
    date += '\n'
    for line in F.readlines():
        if date == line:
            return True
    return False


# check how many days it has been
def keep_tracking(fname):
    F = open(fname, 'r')
    counter = 0
    for line in F.readline():
        counter += 1
    if counter >= 14:
        return False
    else:
        return True

print('Enter new Cramer articles to crawl or nothing to update')
url = input()[:-1]
if url != '':
    daily_tickers = MadMoney(url).get_tickers()
    F = open('Stock_Suggestions.txt', 'a')
    for tickers in daily_tickers:
        print(tickers)
        tickers += '\n'
        F.write(tickers)
    F.close()

F = open('Stock_Suggestions.txt', 'r')
for lines in F.readlines():
    if lines != 'end':
        lines = lines[:-1] # gets rid of the new line character
        fname = lines + '.txt'
        create_db(fname)
        if keep_tracking(fname):
            time.sleep(5)
            get_price(lines)