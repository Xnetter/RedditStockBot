import csv
from settings import alpha_locale_document
from settings import stock_selection

def rebuild_alpha_sheet(char):
	with open(alpha_locale_document, "w+") as alpha: 
		alpha.write(char + " " + '0' + "\n") #We know the csv starts with A
		with open(stock_selection, "r") as stockfile: #open csv
			reader = csv.reader(stockfile) #initialize reader
			for value, row in enumerate(reader, 1): #iterate
				if(row[0]):
					if(row[0][0] != char): #grab first char compare it
						char = row[0][0]
						alpha.write(char + " " + str(value) + "\n") #Take note of character locale


if __name__ == '_main__':
	rebuild_alpha_sheet()