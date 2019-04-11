import asyncio
import datetime
import time
import threading

def foo():
    print (datetime.datetime.now())
    threading.Timer(5, foo).start()


last_time = 0
delay_time = datetime.time(0,0,2)
delay_time = datetime.datetime.strptime(str(delay_time), "%H:%M:%S")

def send_periodic_mex():
    global last_time
    time = datetime.datetime.now()
    if last_time == 0:
        last_time = time
        return 1
    time_diff = time - last_time
    #time_diff = datetime.datetime.strptime(str(time_diff)[:7], "%H:%M:%S")
    print(time_diff)
    print(delay_time)
    print("{} >= {} , {} >= {}".format(time_diff.hour, delay_time.hour, time_diff.minute, delay_time.minute))
    if (time_diff.hour >= delay_time.hour and time_diff.minute >= delay_time.minute):
        print("send Message1") #send message
        return 1
    return 0
send_periodic_mex()
#time.sleep(10)
send_periodic_mex()