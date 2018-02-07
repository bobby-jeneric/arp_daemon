# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from arp_dump import ArpDump


class VMInform:

    @staticmethod
    def send_an_email(sfrom, sto, ssubject, smsg):
        try:
            msg = MIMEText(str)

            msg['Subject'] = ssubject
            msg['From'] = sfrom
            msg['To'] = sto

            s = smtplib.SMTP('localhost')
            s.sendmail(sfrom, [sto], msg.as_string())
            s.quit()
        except Exception as ex:
            ArpDump.printout("ArpScan.do_mail: unable to send mail from {0} to {1}. Reason: {2}".format(sfrom, sto, ex))

class VMInformer:

    @staticmethod
    def inform():
        pass
