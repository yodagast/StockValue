import pandas as pd
dir="D:/BNUSH/name_school-year.tsv"
d=pd.read_csv(dir,delimiter="\t",header=-1)
d.columns=["name","school","year"]
print(d.shape)
d=d.drop_duplicates()
print(d.shape)
tmp=d.groupby(by=["school"]).size().reset_index(name="times")
tmp.sort_values(by=["times"]).to_csv("D:/BNUSH/school-time-all.tsv",sep="\t",index=False)