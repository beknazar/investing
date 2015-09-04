from lxml import html
import requests, csv, urllib2


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

# tickers = getTickers(['screener.ashx?v=111&f=cap_midover,fa_ltdebteq_u1,fa_roa_o5,fa_roe_o15,fa_sales5years_o15,ipodate_more10&ft=4&o=price'])

# print 'All tickers list: ', tickers

def getFCFRate(ticker):
	url = 'http://financials.morningstar.com/ajax/exportKR2CSV.html?callback=?&t=' + ticker
	response = urllib2.urlopen(url)
	cr = csv.reader(response)

	for row in cr:
		print row
		if row and row[0] == 'Free Cash Flow USD Mil':
			print row[1:]
		if row and row[0] = 'Revenue %':
			cr
getFCFRate('INTC')