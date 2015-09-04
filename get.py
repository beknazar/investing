import Quandl

# data = Quandl.get('GOOG/NYSE_IBM', collapse='weekly', authtoken="Xk-qyz6AwsFAuPyyNdyK")
# mydata = Quandl.get("WIKI/AAPL", collapse='annual', start_date='2005-01-01', end_date='2015-08-15')
# print mydata.head()

# input about stock
numShares = 4952
fcfGrowth = 0.05
discountRate = 0.10
perGrowthRate = 0.03

numYears = 10

fcfPrediction = [0]*(numYears + 1)
fcfPrediction[0] = 10847 # current year fcf
discountedSum = 0

for i in range(1,(numYears + 1)):
	fcfPrediction[i] = ( fcfPrediction[i-1]*(1+fcfGrowth) ) 
	discountedSum += fcfPrediction[i] / pow((1+discountRate), i)


perValue = ( fcfPrediction[numYears]*(1+perGrowthRate) ) / (discountRate - perGrowthRate)
discountedPerValue = perValue / pow((1+discountRate), numYears)

totalEquity = discountedPerValue + discountedSum

perShareValue = totalEquity / numShares

print perShareValue

# Xk-qyz6AwsFAuPyyNdyK