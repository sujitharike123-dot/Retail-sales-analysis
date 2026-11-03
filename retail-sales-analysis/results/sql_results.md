### Yearly sales and year-over-year growth (LAG window function)

|   year |   orders |   sales |   yoy_growth_pct |
|-------:|---------:|--------:|-----------------:|
|   2015 |      947 |  479575 |            nan   |
|   2016 |     1019 |  459436 |             -4.2 |
|   2017 |     1295 |  600193 |             30.6 |
|   2018 |     1661 |  722052 |             20.3 |

### Monthly sales, month-over-month growth and 3-month moving average

| month   |   sales |   mom_growth_pct |   moving_avg_3m |
|:--------|--------:|-----------------:|----------------:|
| 2015-01 |   14206 |            nan   |           14206 |
| 2015-02 |    4520 |            -68.2 |            9363 |
| 2015-03 |   55206 |           1121.4 |           24644 |
| 2015-04 |   27625 |            -50   |           29117 |
| 2015-05 |   23644 |            -14.4 |           35492 |
| 2015-06 |   34323 |             45.2 |           28531 |
| 2015-07 |   33782 |             -1.6 |           30583 |
| 2015-08 |   27118 |            -19.7 |           31741 |
| 2015-09 |   81624 |            201   |           47508 |
| 2015-10 |   31453 |            -61.5 |           46731 |
| 2015-11 |   77908 |            147.7 |           63662 |
| 2015-12 |   68167 |            -12.5 |           59176 |
| 2016-01 |   18067 |            -73.5 |           54714 |
| 2016-02 |   11951 |            -33.8 |           32728 |
| 2016-03 |   32339 |            170.6 |           20786 |
| 2016-04 |   34154 |              5.6 |           26148 |
| 2016-05 |   29960 |            -12.3 |           32151 |
| 2016-06 |   23599 |            -21.2 |           29238 |
| 2016-07 |   28608 |             21.2 |           27389 |
| 2016-08 |   36818 |             28.7 |           29675 |
| 2016-09 |   63134 |             71.5 |           42853 |
| 2016-10 |   31012 |            -50.9 |           43655 |
| 2016-11 |   75249 |            142.6 |           56465 |
| 2016-12 |   74544 |             -0.9 |           60268 |
| 2017-01 |   18542 |            -75.1 |           56112 |
| 2017-02 |   22979 |             23.9 |           38688 |
| 2017-03 |   51165 |            122.7 |           30895 |
| 2017-04 |   38680 |            -24.4 |           37608 |
| 2017-05 |   56657 |             46.5 |           48834 |
| 2017-06 |   39724 |            -29.9 |           45020 |
| 2017-07 |   38321 |             -3.5 |           44901 |
| 2017-08 |   30542 |            -20.3 |           36196 |
| 2017-09 |   69193 |            126.6 |           46019 |
| 2017-10 |   59583 |            -13.9 |           53106 |
| 2017-11 |   79066 |             32.7 |           69281 |
| 2017-12 |   95739 |             21.1 |           78130 |
| 2018-01 |   43476 |            -54.6 |           72761 |
| 2018-02 |   19921 |            -54.2 |           53046 |
| 2018-03 |   58863 |            195.5 |           40754 |
| 2018-04 |   35542 |            -39.6 |           38109 |
| 2018-05 |   43826 |             23.3 |           46077 |
| 2018-06 |   48191 |             10   |           42520 |
| 2018-07 |   44825 |             -7   |           45614 |
| 2018-08 |   62838 |             40.2 |           51951 |
| 2018-09 |   86153 |             37.1 |           64605 |
| 2018-10 |   77448 |            -10.1 |           75480 |
| 2018-11 |  117938 |             52.3 |           93846 |
| 2018-12 |   83030 |            -29.6 |           92806 |

### Seasonality - share of all sales by calendar month, ranked

|   month_no |   sales |   share_pct |   sales_rank |
|-----------:|--------:|------------:|-------------:|
|          1 |   94292 |         4.2 |           11 |
|          2 |   59371 |         2.6 |           12 |
|          3 |  197574 |         8.7 |            5 |
|          4 |  136002 |         6   |           10 |
|          5 |  154087 |         6.8 |            7 |
|          6 |  145838 |         6.4 |            8 |
|          7 |  145536 |         6.4 |            9 |
|          8 |  157316 |         7   |            6 |
|          9 |  300103 |        13.3 |            3 |
|         10 |  199496 |         8.8 |            4 |
|         11 |  350162 |        15.5 |            1 |
|         12 |  321480 |        14.2 |            2 |

### Category and sub-category share of sales (window over aggregates)

| category        | sub_category   |   sales |   pct_of_total |   rank_in_category |
|:----------------|:---------------|--------:|---------------:|-------------------:|
| Technology      | Phones         |  327782 |           14.5 |                  1 |
| Furniture       | Chairs         |  322541 |           14.3 |                  1 |
| Office Supplies | Storage        |  219343 |            9.7 |                  1 |
| Furniture       | Tables         |  202811 |            9   |                  2 |
| Office Supplies | Binders        |  200029 |            8.8 |                  2 |
| Technology      | Machines       |  189239 |            8.4 |                  2 |
| Technology      | Accessories    |  164187 |            7.3 |                  3 |
| Technology      | Copiers        |  146248 |            6.5 |                  4 |
| Furniture       | Bookcases      |  113813 |            5   |                  3 |
| Office Supplies | Appliances     |  104618 |            4.6 |                  3 |
| Furniture       | Furnishings    |   89212 |            3.9 |                  4 |
| Office Supplies | Paper          |   76828 |            3.4 |                  4 |
| Office Supplies | Supplies       |   46420 |            2.1 |                  5 |
| Office Supplies | Art            |   26705 |            1.2 |                  6 |
| Office Supplies | Envelopes      |   16128 |            0.7 |                  7 |
| Office Supplies | Labels         |   12348 |            0.5 |                  8 |
| Office Supplies | Fasteners      |    3002 |            0.1 |                  9 |

### Top 10 products by sales

|   sales_rank | product_name                                                                | category        |   sales |   pct_of_total |
|-------------:|:----------------------------------------------------------------------------|:----------------|--------:|---------------:|
|            1 | Canon imageCLASS 2200 Advanced Copier                                       | Technology      |   61600 |           2.72 |
|            2 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies |   27453 |           1.21 |
|            3 | Cisco TelePresence System EX90 Videoconferencing Unit                       | Technology      |   22638 |           1    |
|            4 | HON 5400 Series Task Chairs for Big and Tall                                | Furniture       |   21871 |           0.97 |
|            5 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies |   19823 |           0.88 |
|            6 | GBC Ibimaster 500 Manual ProClick Binding System                            | Office Supplies |   19025 |           0.84 |
|            7 | Hewlett Packard LaserJet 3310 Copier                                        | Technology      |   18840 |           0.83 |
|            8 | HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | Technology      |   18375 |           0.81 |
|            9 | GBC DocuBind P400 Electric Binding System                                   | Office Supplies |   17965 |           0.79 |
|           10 | High Speed Automatic Electric Letter Opener                                 | Office Supplies |   17030 |           0.75 |

### Region by category sales matrix

| region   |   furniture |   office_supplies |   technology |   total |   pct_of_total |
|:---------|------------:|------------------:|-------------:|--------:|---------------:|
| West     |      245348 |            217467 |       247405 |  710220 |           31.4 |
| East     |      206180 |            199941 |       263117 |  669237 |           29.6 |
| Central  |      160317 |            163590 |       168739 |  492647 |           21.8 |
| South    |      116531 |            124425 |       148195 |  389151 |           17.2 |

### Top 10 states by sales

|   sales_rank | state        | region   |   sales |   pct_of_total |
|-------------:|:-------------|:---------|--------:|---------------:|
|            1 | California   | West     |  446306 |           19.7 |
|            2 | New York     | East     |  306361 |           13.5 |
|            3 | Texas        | Central  |  168573 |            7.5 |
|            4 | Washington   | West     |  135207 |            6   |
|            5 | Pennsylvania | East     |  116277 |            5.1 |
|            6 | Florida      | South    |   88437 |            3.9 |
|            7 | Illinois     | Central  |   79237 |            3.5 |
|            8 | Michigan     | Central  |   76136 |            3.4 |
|            9 | Ohio         | East     |   74849 |            3.3 |
|           10 | Virginia     | South    |   70637 |            3.1 |

### Customer concentration - sales by customer quintile (NTILE)

|   quintile |   customers |            sales |   pct_of_sales |
|-----------:|------------:|-----------------:|---------------:|
|          1 |         159 |      1.09614e+06 |           48.5 |
|          2 |         159 | 530068           |           23.4 |
|          3 |         159 | 350389           |           15.5 |
|          4 |         158 | 204262           |            9   |
|          5 |         158 |  80399           |            3.6 |

### Segment performance with average order value (CTE)

| segment     |   orders |            sales |   avg_order_value |
|:------------|---------:|-----------------:|------------------:|
| Consumer    |     2537 |      1.14806e+06 |            452.53 |
| Corporate   |     1491 | 688494           |            461.77 |
| Home Office |      894 | 424701           |            475.06 |

### Shipping speed by ship mode

| ship_mode      |   orders |   pct_of_orders |   avg_days_to_ship |
|:---------------|---------:|----------------:|-------------------:|
| Same Day       |      261 |             5.3 |                0   |
| First Class    |      772 |            15.7 |                2.2 |
| Second Class   |      944 |            19.2 |                3.2 |
| Standard Class |     2945 |            59.8 |                5   |

