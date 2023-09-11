#!/usr/bin/env python3
import logging
import json
import os
import time
import urllib.request
import html.parser

BVB_URL = "https://m.bvb.ro/FinancialInstruments/Indices/IndicesProfiles.aspx?i=BET"
CRAWLER_CACHE = "crawler_bvb_cache.json"

TABLE_ID = "gvTD"
COL_SYMBOL = "Simbol"
COL_PRICE = "Pret"
COL_WEIGHT = "Pondere (%)"

STATE_INIT = 0
STATE_TABLE = 1
STATE_THEAD = 2
STATE_TH = 3
STATE_TBODY = 4
STATE_TD = 5

class BvbParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.state = STATE_INIT
        self.columns = []
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if self.state == STATE_INIT:
            if tag == "table":
                for key, val in attrs:
                    if key == "id" and val == TABLE_ID:
                        self.state = STATE_TABLE
        elif self.state == STATE_TABLE:
            if tag == "thead":
                self.state = STATE_THEAD
        elif self.state == STATE_THEAD:
            if tag == "th":
                self.state = STATE_TH
            elif tag == "tbody":
                self.state = STATE_TBODY
        elif self.state == STATE_TBODY:
            if tag == "tr":
                self.rows.append([])
            elif tag == "td":
                self.state = STATE_TD

    def handle_endtag(self, tag):
        if tag == "table":
            self.state = STATE_INIT

    def handle_data(self, data):
        if self.state == STATE_TH:
            self.columns.append(data.strip())
            self.state = STATE_THEAD
        elif self.state == STATE_TD:
            if len(self.rows) > 0:
                self.rows[-1].append(data.strip())
            self.state = STATE_TBODY

def crawl():
    crtTs = time.time()
    if os.path.isfile(CRAWLER_CACHE):
        with open(CRAWLER_CACHE) as fin:
            cache = json.load(fin)
            if "ts" in cache and "data" in cache and cache["ts"] + 300 > crtTs:
                logging.info("loading BVB data from cache")
                return cache["data"]
    with urllib.request.urlopen(BVB_URL) as response:
        content = response.read()
        parser = BvbParser()
        parser.feed(content.decode())
        parser.close()

        if len(parser.columns) < 3 or len(parser.rows) < 5:
            logging.error(f"Nu s-au putut obtine date de la url-ul '{BVB_URL}'")
            return None

        colSymbol = None
        colPrice = None
        colWeight = None

        for idx, col in enumerate(parser.columns):
            if col == COL_SYMBOL:
                colSymbol = idx
            elif col == COL_PRICE:
                colPrice = idx
            elif col == COL_WEIGHT:
                colWeight = idx
        if colSymbol is None:
            logging.error(f"Nu s-a gasit coloana {COL_SYMBOL}")
            return None
        if colPrice is None:
            logging.error(f"Nu s-a gasit coloana {COL_PRICE}")
            return None
        if colWeight is None:
            logging.error(f"Nu s-a gasit coloana {COL_WEIGHT}")
            return None

        result = {}
        for row in parser.rows:
            if len(row) < max(colSymbol, colPrice, colWeight):
                logging.error("Tabelul cu datele nu are formatul corect")
                return None
            symbol = row[colSymbol]
            price = row[colPrice].replace(",", ".")
            weight = row[colWeight].replace(",", ".")
            try:
                price = float(price)
            except ValueError:
                logging.error(f"Pretul {price} pentru simbolul {symbol} nu este un numar valid")
                return None
            try:
                weight = float(weight)
            except ValueError:
                logging.error(f"Ponderea {weight} pentru simbolul {weight} nu este un numar valid")
            result[symbol] = {"price": price, "weight": weight}
        with open(CRAWLER_CACHE, "w") as fout:
            json.dump({"ts": crtTs, "data": result}, fout)
        return result
    

if __name__ == "__main__":
    result = crawl()
    print(result)