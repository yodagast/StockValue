import tushare as ts
pro = ts.pro_api('44e26f14d14da304ac82045a39bf644ad0b0dc301d6a5cbf907a1907')
df = pro.query('daily', ts_code='601166.SH', start_date='20200601', end_date='20200830')
df.hist(bins=5)
