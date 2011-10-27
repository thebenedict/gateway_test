RapidSMS HTTP Gateway Tester
============================

When using RapidSMS with an HTTP gateway, messages usually flow like this:

    Handset<--->Gateway<-->RapidSMS

This is a tool for measuring the time messages take to travel in each 
direction, and for counting messages dropped along the way. It uses Scripting Layer for Android (SL4A), and was written by Michael Benedict.

Installation requires an Android phone, a RapidSMS instance, and 2-way HTTP 
gateway service. Logs are written to a CSV file on the phone's SD card.

**Installation**

- Install SL4A on your Android phone by scanning the QR code here:
  http://code.google.com/p/android-scripting/
- Install the Python interpreter for SL4A:
  http://code.google.com/p/android-scripting/wiki/InstallingInterpreters
- Clone ``gateway_test`` from github and copy the app into into a RapidSMS project directory:

    $ git clone git://github.com/thebenedict/gateway_test.git

- Edit the config section of ``gwtest.py``, and copy it to your phone at:
  /mnt/sdcard/sl4a/scripts/gwtest.py
- Add ``gateway_test`` to ``INSTALLED_APPS`` in settings.py, and restart your webserver

When you're ready, load some airtime on your SIM, start SL4A, and run ``gwtest.py``. Note that this script currently doesn't use a wake lock (WTF!), and will stop if the phone goes to sleep. It's designed to be used on a phone that is plugged in and set to not sleep while charging. More on this at:
  http://code.google.com/p/android-scripting/wiki/FAQ#My_script_stops_working_when_the_screen_turns_off!_WTF?

Kill the script when you've had enough, and find your log file in your phone's
SL4A directory.

**Log File Column Headers**

- Message status -- SENT/FAILED/RECIEVED, where FAILED means the phone could not send
- Direction -- MO or MT
- Message number -- counts up from 1
- Date sent from phone
- Time sent from phone
- Date arrived at Rapid
- Time arrived at Rapid
- M/G -- delay in seconds between the mobile and gateway as measured by Rapid
- Date gateway reply arrived on phone
- Time gateway reply arrived on phone
- G/M -- delay in seconds between the gateway and mobile

Questions, suggestions and improvements (especially improvements!) are very welcome. If you take some data please do share.
