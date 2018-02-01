# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

class VMInform:

    @staticmethod
    def send_an_email(sfrom, sto, ssubject, smsg):
        msg = MIMEText(str)

        msg['Subject'] = ssubject
        msg['From'] = sfrom
        msg['To'] = sto

        s = smtplib.SMTP('localhost')
        s.sendmail(sfrom, [sto], msg.as_string())
        s.quit()


class VMInformer:

    @staticmethod
    def inform():
        pass
