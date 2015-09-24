from lxml import html
import requests, csv, urllib2, json
from operator import itemgetter

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
	if len(cr) < 111:
		return -1
	return cr

def getAverage(ticker, line):
	cr = getCSV(ticker)
	if cr == -1 or line >= len(cr):
		return 0
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
	return 0

def getMin(ticker, line):
	cr = getCSV(ticker)
	if cr == -1 or line >= len(cr):
		return 0
	fcf = cr[line]
	fcf = [s.replace(',','') for s in fcf] # ',' -> ''
	fcf = filter(None, fcf[1:])
	fcf = map(float, fcf)
	return min(fcf)

def saveToCSV(startingURL):
	tickers = getTickers(startingURL)
	print tickers
	for ticker in tickers:
		csvList[ticker] = {'fcf': int(getAverage(ticker, 15)),
							'grossMargin': getAverage(ticker, 23),
							'fcfGrowth': getAverage(ticker, 67),
							'fcfPsales': getAverage(ticker, 69),
							'minROE': getMin(ticker, 37),
							'epsRate': getAverage(ticker, 62)}
	with open('data.json', 'w') as fp:
		json.dump(csvList, fp)
	print 'Done!:', len(csvList), 'stocks'

saveToCSV(['screener.ashx?v=111&f=fa_pe_low,sh_insidertrans_verypos&ft=4'])

with open('data.json', 'r') as fp:
    csvList = json.load(fp)

w = csv.writer(open("output.csv", "w"))

w.writerow(['Ticker', 'fcfGrowth', 'fcfPsales', 'fcf', 'grossMargin', 'minROE', 'epsRate'])
for k in csvList:
	w.writerow([k, csvList[k]['fcfGrowth'],
		csvList[k]['fcfPsales'],
		csvList[k]['fcf'],
		csvList[k]['grossMargin'], 
		csvList[k]['minROE'],
		csvList[k]['epsRate']])
# mylist = sorted(csvList, key=itemgetter('fcfGrowth', 'fcfPsales', 'fcf'))

# print 'Free Cash Flow USD Mil: ', int(getAverage('AAPL', 15))
# print 'Gross Margin: ', getAverage('AAPL', 23)
# print 'Free Cash Flow Growth % YOY: ', getAverage('AAPL', 67)
# print 'Free Cash Flow/Sales %: ', getAverage('AAPL', 69)

