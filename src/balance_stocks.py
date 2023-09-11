import logging
import math
import itertools
import heapq

from src import portfolio

class ProgressBar:
    def __init__(self, maxVal, fillChar="#", nrElts=32):
        self.val = 0
        self.maxVal = maxVal
        self.fillChar = fillChar
        self.nrElts = nrElts
        self.elts = -1

    def next(self):
        self.val += 1
        elts = self.nrElts * self.val // self.maxVal
        if elts != self.elts:
            self.elts = elts
            line = "[" + (self.fillChar * self.elts) + (" " * (self.nrElts - self.elts)) + "] " + f"{self.val} / {self.maxVal}"
            print(f"\r{line}", end="")

def relativeError(s, count, portfolioValue, investedSum):
    weight = s.price * (s.initialCount + count[s.symbol]) / (portfolioValue + investedSum)
    return (weight - s.normWeight) / s.normWeight

def balanceStocks(p: portfolio.Portfolio, investedSum: float, tradingFee: float, minFee: float):
    if investedSum * tradingFee < minFee:
        logging.error("Suma investita este prea mica")
        return False
    investedSum = investedSum * (1.0 - tradingFee)
    totalWeight = 0.0
    portfolioValue = 0.0
    for s in p.stocks:
        if s.price is None:
            logging.error(f"Pretul nu a fost setat pentru simbolul {s.symbol}")
            return False
        if s.weight is None:
            logging.error(f"Ponderea nu a fost setata pentru simbolul {s.symbol}")
            return False
        totalWeight += s.weight
        portfolioValue += s.price * s.initialCount
    minCount = {s.symbol: math.ceil(minFee / tradingFee / s.price) for s in p.stocks}
    for s in p.stocks:
        s.normWeight = s.weight / totalWeight

    bestCount = None
    bestError = None
    bar = ProgressBar(2**len(p.stocks) - 1)
    for subset in itertools.chain.from_iterable(itertools.combinations(p.stocks, k) for k in range(1, len(p.stocks) + 1)):
        bar.next()
        count = {s.symbol: minCount[s.symbol] for s in subset}
        totalInvested = sum(p.get(symbol).price * cnt for symbol, cnt in count.items())
        if totalInvested >= investedSum:
            continue
        h = []
        for s in subset:
            heapq.heappush(h, (relativeError(s, count, portfolioValue, investedSum), s))
        while len(h) > 0:
            _, s = heapq.heappop(h)
            if totalInvested + s.price >= investedSum:
                continue
            count[s.symbol] += 1
            totalInvested += s.price
            heapq.heappush(h, (relativeError(s, count, portfolioValue, investedSum), s))
        error = 0.0
        for s in p.stocks:
            weight = s.price * (s.initialCount + count.get(s.symbol, 0)) / (portfolioValue + totalInvested)
            error += ((weight - s.normWeight) / s.normWeight) ** 2
        if bestError is None or error < bestError:
            bestError = error
            bestCount = count
    print()

    if bestCount is None:
        return False
    for symbol, value in bestCount.items():
        s = p.get(symbol)
        s.count = s.initialCount + value
    return True