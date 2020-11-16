### StockValue
#### data warehouse
- jd_data : curl data from jd, store in local file system(lfs)
    - unrar data and append data into lfs
    - store data into spark delta format(parquet)
- ts_data: curl data from tushare, store into lfs
    - get 
- realtime_data: curl data from sina eta

#### stock 
- TimeSelector

- StockSelector

#### index 
- index enhence
- other funds

#### visualization
- single feature visualization
- realtime visualization

#### trader
- auto trader