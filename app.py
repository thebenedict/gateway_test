#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

from rapidsms.apps.base import AppBase
from datetime import datetime

class App(AppBase):
    """
    Reply to gateway test messages
    """

    def handle(self, message):
        if not message.text.startswith("gwt,M"):
            return False

        reply = message.text.replace("MO","MT")
        tokens = message.text.split(",")
        delay = self.getDelay(tokens[3], tokens[4])
        datenow = datetime.now().date()
        timenow = datetime.now().time()
        reply = reply + ",%s,%s,%s" % (datenow, timenow, delay)
        message.respond(reply)
        return True

    def getDelay(self, date_string, time_string):
        sent_datetime_string = "%s@%s" % (date_string, time_string)
        sent_datetime = datetime.strptime(sent_datetime_string,
                                          "%Y-%m-%d@%H:%M:%S.%f")
        delta = datetime.now() - sent_datetime
        return (delta.microseconds + 
                (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6
