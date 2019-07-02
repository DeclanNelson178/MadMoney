


class PriceCrawler:
    def __init__(self, ticker):
        self.url = 'https://www.google.com/search?q=' + ticker + '&tbm=fin#scso=_727XXLqbOs2KggfIz7bYCQ2:0,_j3DXXPqiA-jm5gLhlYSgCA2:0'

    def price(self):
        return 0


class Stock:

    def __init__(self, ticker):
        self.ticker = ticker
        print('You have created a new stock called ' + ticker)

    def get_price(self):
        crawler = PriceCrawler(self.ticker)
        price = crawler.price()
        print(price)


IBM = Stock('IBM')
print('----------------')
IBM.get_price()



