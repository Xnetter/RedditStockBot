
import csv
import itertools
from iexfinance.stocks import Stock
from settings import iex_auth_token
from settings import stock_selection
from settings import alpha_locale_document


#ignore = [] #Ticker Confusions that should simply be ignored. #Automated feature
class Stocks():

	def __init__(self, stockTag):
		self.tag = stockTag
		self.name = None
		self.current = None
		self.generateName()
		if(self.name):#Only search for stock data if stock can be found
			self.scrape()


	def generateName(self):
		with open(alpha_locale_document, "r") as alpha_locale:
			print(self.tag)
			row = alpha_locale.read().split(self.tag[0])[1].split("\n")[0].strip()

			with open(stock_selection, "r") as stockfile:	
				csvreader = csv.reader(stockfile)
				for row in csvreader: #start at the row specified and continue until the end.
					if(self.tag == row[0]):# (automated version extension) --> and (self.tag not in ignore)): #if entry exists in nasdaq file, success
						self.name = row[1].replace('"', "") #trailing quotes
	
	def __eq__(self, other): #allows for the removal of duplicates
		return (self.name == other.name) and (other.tag == self.tag)

	def scrape(self):
		share = Stock(self.tag, token = iex_auth_token) #create an iexfinance object using ticker for data extraction
		self.price = "%.2f" % float(share.get_price())
		#EXTRA INFORMATION IF DESIRED
		# self.headline = share.get_news()[0]['headline']
		# self.headline_hyper = share.get_news()[0]['url']
		# self.open = "%.2f" % float(share.get_open())
		# self.close = "%.2f" % float(share.get_close())
		# self.year_high = "%.2f" % float(share.get_years_high())
		# self.year_low = "%.2f" % float(share.get_years_low())
		self.year_change = ("%.2f" % (float(share.get_ytd_change())*100)) + " percent change."
	
	def rundown(self): #Mainly for testing purposes, to ensure data retrieval.
		print(self.price)
		#EXTRA DATA
		# print(self.headline)
		# print(self.open)
		# print(self.close)
		# print(self.year_high)
		# print(self.year_low)
		print(self.year_change)