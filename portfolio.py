import os
import csv
import logging

class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.initialCount = 0
        self.count = 0
        self.price = None
        self.weight = None

class Portfolio:
    COL_SYMBOL = "Simbol"
    COL_COUNT = "Cantitate"
    COL_PRICE = "Pret"
    COL_WEIGHT = "Pondere"

    def __init__(self):
        self.stocks = []

    def readStocks(self, fpath):
        if not os.path.isfile(fpath):
            logging.error(f"Fisierul cu portofoliul '{fpath}' nu exista")
            return False
        with open(fpath) as fin:
            reader = csv.DictReader(fin)
            for row in reader:
                for col in [Portfolio.COL_SYMBOL, Portfolio.COL_COUNT, Portfolio.COL_PRICE, Portfolio.COL_WEIGHT]:
                    if col not in row:
                        logging.error(f"Coloana '{col}' lipseste din fisierul cu portofoliul '{fpath}'")
                        return False
                symbol = row[Portfolio.COL_SYMBOL].strip()
                if len(symbol) > 0:
                    s = Stock(symbol)
                    try:
                        s.initialCount = int(row[Portfolio.COL_COUNT].strip())
                    except ValueError:
                        logging.error(f"Coloana '{Portfolio.COL_COUNT}' trebuie sa contina numere intregi. Valoarea '{row[Portfolio.COL_COUNT]}' este invalida.")
                        return False
                    s.count = s.initialCount
                    if len(row[Portfolio.COL_PRICE].strip()) > 0:
                        try:
                            s.price = float(row[Portfolio.COL_PRICE].strip())
                        except ValueError:
                            logging.error(f"Coloana '{Portfolio.COL_PRICE}' trebuie sa contina numere reale (separatorul este '.'). Valoarea '{row[Portfolio.COL_PRICE]}' este invalida.")
                            return False
                    if len(row[Portfolio.COL_WEIGHT].strip()) > 0:
                        try:
                            s.price = float(row[Portfolio.COL_WEIGHT].strip())
                        except ValueError:
                            logging.error(f"Coloana '{Portfolio.COL_WEIGHT}' trebuie sa contina numere reale(separatorul este '.'). Valoarea '{row[Portfolio.COL_WEIGHT]}' este invalida.")
                            return False
                    self.stocks.append(s)
        if len(self.stocks) == 0:
            logging.error(f"Fisierul cu portofoliul '{fpath}' trebuie sa contina cel putin un simbol")
            return False
        return True

    def display(self):
        COLUMNS = ["Simbol", "Recomandare", "Cantitate", "Pret", "Pondere"]
        data = []
        for s in self.stocks:
            recommendation = ""
            if s.count > s.initialCount:
                recommendation = f"+{s.count - s.initialCount}"
            elif s.count < s.initialCount:
                recommendation = f"{s.count - s.initialCount}"
            if s.initialCount == s.count:
                count = str(s.count)
            else:
                count = f"{s.initialCount} -> {s.count}"

            data.append((
                s.symbol,
                recommendation,
                count,
                str(s.price) if s.price is not None else "",
                str(s.weight) if s.weight is not None else "",
            ))

        SIZES = [len(col) + 1 for col in COLUMNS]
        for row in data:
            for i in range(len(SIZES)):
                if len(row[i]) > SIZES[i]:
                    SIZES[i] = len(row[i])
        HLINE = "+" + "+".join("-" * s for s in SIZES) + "+"
        print(HLINE)
        print("|" + "|".join("%*s" % (size, col) for size, col in zip(SIZES, COLUMNS)) + "|")
        print(HLINE)
        for row in data:
            print("|" + "|".join("%*s" % (size, col) for size, col in zip(SIZES, row)) + "|")
        print(HLINE)

    def updatePrice(self, crawlData):
        for s in self.stocks:
            if s.symbol in crawlData:
                s.price = crawlData[s.symbol]["price"]

    def updateWeight(self, crawlData):
        for s in self.stocks:
            if s.symbol in crawlData:
                s.weight = crawlData[s.symbol]["weight"]