import time
import urllib
import android
from datetime import datetime

'''
RapidSMS HTTP Gateway Tester - SL4A Script

This file is not run by RapidSMS. It should be run from an Android
phone via SL4A (http://code.google.com/p/android-scripting/).

Edit the config section below and then put this file on your phone at:
    /mnt/sdcard/sl4a/scripts/gwtest.py
See the readme for more detailed instructions.

Built by Michael Benedict
'''

##Config##
GATEWAY_PHONE = #Your gateway phone number goes here
SEND_INTERVAL = 600 #Test interval in seconds
##End config##

def getDelay(date_string, time_string):
    '''
    Returns the time, in seconds, between when a reply was sent by
    Rapid and when it hit the phone. Note that it assumes the clock on
    the Android phone is synchronized with the clock on the server
    running RapidSMS
    '''
    sent_datetime_string = "%s@%s" % (date_string, time_string)
    sent_datetime = datetime.strptime(sent_datetime_string,
                                      "%Y-%m-%d@%H:%M:%S.%f")
    delta = datetime.now() - sent_datetime
    return (delta.microseconds + 
            (delta.seconds + delta.days * 24 * 3600) * 10**6) / 10**6

def processReceived(message, logname):
    '''
    Append current time, date, and latency to a response message
    received from Rapid.
    '''
    tokens = message['body'].split(",")
    delay = getDelay(tokens[5], tokens[6])
    datenow = datetime.now().date()
    timenow = datetime.now().time()
    print "Received a message: %s" % message['body']
    log = open(logname, 'a')
    log.write("RECEIVED," + message['body'].strip('gwt,') + 
              ",%s,%s,%s\n" % (datenow, timenow, delay))
    log.close()
    droid.smsMarkMessageRead([message['_id']], 1)

def sendFromPhone(logname, sent_count):
    '''
    Sends a test message from an Android phone to RapidSMS, as:
        gwt,MO,<sent_count>,<current date>,<current_time>
    and updates the log file with this information.
    '''
    datenow = datetime.now().date()
    timenow = datetime.now().time()
    text = "gwt,MO,%s,%s,%s" % (sent_count, datenow, timenow)
    try:
        droid.smsSend(GATEWAY_PHONE, text)
        print "Message %s sent at %s" % (sent_count, timenow)
        log = open(logname, 'a')
        log.write("SENT," + text.strip('gwt,') + '\n')
        log.close()
        sent_count += 1
        return sent_count
    except:
        print "Message %s failed to send at %s %s" % (sent_count, datenow,
                                                      timenow)
        log = open(logname, 'a')
        log.write("FAILED," + text.strip('gwt,') + '\n')
        log.close()
        return sent_count

def runTest(droid):
    '''
    Write header to the log file and run the main loop. Identifies
    test messages as beginning with "gwt,M"
    '''
    logname = "smslog_%s.csv" % \
              "".join(d for d in str(datetime.now()) if d.isdigit())[4:]
    log = open(logname, 'a')
    log.write("Status,Direction,#,Send Date,Send Time,Gateway Date,"
              "Gateway Time,M/G,Received Date,Received Time,G/M\n")
    log.close()
    timer = 0
    sent_count = 1
    while True:
        messages = droid.smsGetMessages(1).result
        for m in messages:
            if m['body'].startswith("gwt,M"):
                processReceived(m, logname)
        if timer % SEND_INTERVAL <= 1:
            sent_count = sendFromPhone(logname, sent_count)
        else:
            #bit of a hack to put this in an else clause, but the message
            #send takes about 2 seconds on my device
            time.sleep(2)
        timer += 2

if __name__ == '__main__':
    droid = android.Android()
    runTest(droid)
