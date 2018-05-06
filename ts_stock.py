import os,sys
import tushare as ts
import pandas as pd
import numpy as np
df=ts.get_stock_basics()
industry=pd.unique(df["industry"])
if(os.path.exists("industry.csv")==False):
    f=open("industry.csv","w")
    for d in industry:
        f.write(d + "\n")
    f.close()
if(os.path.exists("col.csv")==False):
    f = open("col.csv", "w")
    for col in df.columns:
        f.write(col + "\n")
    f.close()

res=pd.DataFrame()
for ind in industry:
    cond=(df.industry==ind) & (df.pe>0.1) &(df.pb<3.0) & (df.pe<8.0)
    bank=df[["name","industry","pe","pb","esp","bvps","profit"]][cond].sort_values(by="pe")
    tmp=bank.head(20)
    res=pd.concat([res,tmp])
res.to_csv("res.csv",sep="\t")
