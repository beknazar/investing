from lxml import html
import requests, csv, urllib2


csvList = dict()

def getTickers(url):
	nextURL = url
	tickers = []
	while nextURL:
		print 'loading: ', 'http://finviz.com/' + nextURL[-1]
		page = requests.get('http://finviz.com/' + nextURL[-1])
		tree = html.fromstring(page.text)

		# This will get list of tickers
		tickers += tree.xpath('//a[@class="screener-link-primary"]/text()')
		#This will create a list of prices
		# prices = tree.xpath('//a[@class="screener-link"]/text()')
		nextURL = tree.xpath('//a[@class="tab-link" and contains(., "next")]/@href')

		# print 'Tickers: ', tickers
		# print 'nextURL: ', nextURL
	return tickers

def getCSV (ticker):
	if ticker in csvList:
		return csvList[ticker]['csv']
	url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?callback=?&t=' + ticker
	response = urllib2.urlopen(url)
	cr = list(csv.reader(response))
	csvList[ticker] = {'csv': cr}
	return cr

def getAverage(ticker, line):
	cr = getCSV(ticker)
	fcf = cr[line]
	# print atof('123,456') 
	fcf = [s.replace(',','') for s in fcf] # ',' -> ''
	# print fcf
	fcf = filter(None, fcf[1:])
	fcfLength = len(fcf)
	if fcfLength > 5:
		fcf = map(float, fcf)
		# print fcf
		avgRate = sum(fcf) / float(fcfLength)
	return avgRate

ticker = 'AAPL'
csvList[ticker] = {'fcf': int(getAverage(ticker, 15)),
					'grossMargin': getAverage(ticker, 23),
					'fcfGrowth': getAverage(ticker, 67),
					'fcfPsales': getAverage(ticker, 69)}


w = csv.writer(open("output.csv", "w"))
for key, val in csvList.items():
    w.writerow([key, val])
# print 'Free Cash Flow USD Mil: ', int(getAverage('AAPL', 15))
# print 'Gross Margin: ', getAverage('AAPL', 23)
# print 'Free Cash Flow Growth % YOY: ', getAverage('AAPL', 67)
# print 'Free Cash Flow/Sales %: ', getAverage('AAPL', 69)

