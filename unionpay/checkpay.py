import os,subprocess,sched
import time,datetime
from threading import Timer
from datetime import date

def get_checkpay(path,list_mech=None,str_org='b0103'):
    today=date.today().strftime("%Y%m%d")
    if (os.path.exists(path+today) == False):
        os.mkdir(path+today)
    for mech in list_mech:
        file_name="{0}-{1}-{2}.tmp".format(str_org,mech,today)
        if(os.path.isfile(path+today+"/"+file_name)):
            rm_file="rm {0}".format(path+file_name)
            os.popen(rm_file).read()
        file=open(path+today+"/"+file_name,mode="w+")
        str_shell = '''cat `ls /home/b0103/*ACOM`|grep "{1}"'''.format(str_org,mech)
        records=os.popen(str_shell).read().split("\r\n")
        for r in records:
            #s=r[25:30]+"|"+r[31:41]+"|"+r[62:74]+"|"+r[106:112]+"|"+r[118:126]+"|"+r[127:142]
            s=r[127:142]+"|"+r[118:126]+"|"+r[25:30]+"|"+r[106:112]+"|1|"+r[62:74]+"|"+r[31:41]
            file.write(s+"\n")
        file.close()

def main():
    str_org = 'b0103'
    mech_list = ["103510741110001", "103510741110002", "103510741110003", "103510741110004", "103510741110005"]
    file_path="/home/cap/yhuang/"
    if(os.path.exists(file_path)==False):
        os.mkdir(file_path)
    get_checkpay(list_mech=mech_list,str_org=str_org,path=file_path)

main()