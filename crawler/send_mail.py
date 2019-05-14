from datetime import date
import logging

import smtplib,os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from smtplib import SMTP_SSL
#from email.MIMEMultipart import MIMEMultipart

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def attach_message(message ,date ,path=None):
    # path="../ticks/"
    # path="/home/ywb/yhuang/"+today+"/"
    if (os.path.exists(path)):
        for root, dirs, files in os.walk(path):
            for name in files:
                if(name.format(date ) <1):
                    continue
                dd =os.path.join(root, name)
                logger.info(dd +"|||||||||||||| " +name)
                try:
                    part = MIMEApplication(open(dd ,"rb").read())
                    part.add_header('Content-Disposition', 'attachment', filename=name)
                    message.attach(part)
                except IOError:
                    logger.error("error attach file {}".format(dd))
                    continue
    else:
        logger.error("file not found")


def send_multipart_mail(d):
    try:
        smtpObj = smtplib.SMTP(d["mail_host"])
        # smtpObj = SMTP_SSL(d["mail_host"])
        # smtpObj.connect(d["mail_host"])
        # smtpObj.set_debuglevel(1)
        smtpObj.ehlo(d["mail_host"])
        smtpObj.login(d["mail_user"], d["mail_pass"])
        message = MIMEMultipart()
        message['From'] = d["sender"]
        message['To'] = d["receiver"]
        message['Subject'] = '{0}-数据统计'.format(date.today().strftime("%Y%m%d"))
        attach_message(message)
        smtpObj.sendmail(d["sender"], d["receiver"], message.as_string())
        logger.info('success send email {}'.format())
        smtpObj.quit()
    except smtplib.SMTPException:
        logger.error("error {}" ,smtplib.SMTPException)

def send_mail():
    d={}
    d["mail_host"]="smtp.qq.com"# "s  mtp.unionpay.com"
    d["mail_user"]="shellhys@qq.com"
    d["mail_pass"]="wbljlarhnupsebdg"
    d["sender"]="shellhys@qq.com"# "h  uangyong@unionpay.com"
    d["receiver"]="shellhys@qq.com"# "h  uangyong@unionpay.com"#"shellhys@qq.com"
    send_multipart_mail(d)
