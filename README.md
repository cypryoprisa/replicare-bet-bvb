# replicare-bet-bvb
Programul curent se adresează persoanelor care doresc să replice parțial sau total indicele BET, investind în mod regulat.

Programul primește deținerile actuale, sub forma unui fișier .csv, respectiv suma care se dorește investită și recomandă utilizatorului ce acțiuni să cumpere, pentru a obține un portofoliu cât mai echlibrat, respectând ponderile din indicele BET.

# Utilizare

## Specificarea portofoliului curent
Faceți o copie a fișierului `portofoliu.csv.template`, numită `portofoliu.csv` și editați-o cu Excel sau un alt editor de spreasheet-uri.

Păstrați doar liniile cu simbolurile pe care le dețineți sau doriți să le dețineți și completați cantiatea curentă pe care o aveți în portofoliu. Puteți lăsa necompletate coloanele `Pret` si `Pondere`, în mod implicit programul va obține valorile de pe site-ul [BVB](https://m.bvb.ro/FinancialInstruments/Indices/IndicesProfiles.aspx?i=BET).

## Rularea programului

Rulați script-ul `replicare_bet.py` dând ca argument suma pe care doriți să o investiți (în RON). Pentru a rula script-ul e nevoie să aveți instalat Python 3.7 sau mai nou.

Exemplu:

```
$ python3 replicare_bet.py 5000
Suma de investit: 2500.0
Comision broker: 0.43% + 1.5 RON
Suma minima / tranzactie: 500 RON

[################################] 1023 / 1023
+-------+------------+----------+------+----------------+----------------------+---------------------+---------------+-----------------------+
| Simbol| Recomandare| Cantitate|  Pret| Pondere BET (%)| Pondere BET norm. (%)| Pondere detinuta (%)|  Diferenta (%)| Diferenta relativa (%)|
+-------+------------+----------+------+----------------+----------------------+---------------------+---------------+-----------------------+
|    TLV|         +60|   0 -> 60| 22.44|           24.58|                 27.47|        0.00 -> 27.11|-27.47 -> -0.36|       -100.00 -> -1.32|
|    SNP|       +1674| 0 -> 1674|0.5705|           17.31|                 19.35|        0.00 -> 19.23|-19.35 -> -0.12|       -100.00 -> -0.61|
|    H2O|          +8|    0 -> 8| 114.1|           16.81|                 18.79|        0.00 -> 18.38|-18.79 -> -0.41|       -100.00 -> -2.18|
|    SNG|         +11|   0 -> 11|  42.5|            7.99|                  8.93|         0.00 -> 9.41|  -8.93 -> 0.48|        -100.00 -> 5.40|
|    BRD|         +25|   0 -> 25| 14.82|            6.71|                  7.50|         0.00 -> 7.46| -7.50 -> -0.04|       -100.00 -> -0.53|
|    SNN|          +7|    0 -> 7|  46.9|            4.65|                  5.20|         0.00 -> 6.61|  -5.20 -> 1.41|       -100.00 -> 27.19|
|     FP|        +748|  0 -> 748| 0.391|            3.55|                  3.97|         0.00 -> 5.89|  -3.97 -> 1.92|       -100.00 -> 48.41|
|      M|         +65|   0 -> 65| 4.525|            2.78|                  3.11|         0.00 -> 5.92|  -3.11 -> 2.81|       -100.00 -> 90.59|
|    TGN|            |         0|  18.1|            2.74|                  3.06|         0.00 -> 0.00| -3.06 -> -3.06|     -100.00 -> -100.00|
|   DIGI|            |         0|  35.9|            2.36|                  2.64|         0.00 -> 0.00| -2.64 -> -2.64|     -100.00 -> -100.00|
+-------+------------+----------+------+----------------+----------------------+---------------------+---------------+-----------------------+
Suma totala cheltuita: 4967.11 + comision 32.29
```

Argumentele opționale ale programului permit să specificați:

* `-f` numele fișierului csv din care se vor citi deținerile curente; valoarea implicită este `portofoliu.csv`
* `-p` nu se va încerca obținerea prețurilor de pe internet, se vor folosi cele din fișierul csv
* `-w` nu se va încerca obținerea ponderilor în BET de pe internet, se vor folosi ponderile din fișierul csv
* `-t` comisionul broker-ului, în procente; valoarea implicită este 0.43%
* `-x` comisionul fix al broker-ului, per tranzacție; valoarea implicită este 1.5 RON
* `-m` suma minimă pentru o tranzacție, în RON; valoarea implicită este 500; script-ul va sugera cumpărarea unui simbol doar dacă se atinge sau depășește suma minimă

La o sumă minimă per tranzacție de 500 RON, pentru o acțiune care costă 50 RON bucata, programul fie vă va propune să cumpărați 10 sau mai multe, fie nu va recomanda cumpărarea acestei acțiuni.