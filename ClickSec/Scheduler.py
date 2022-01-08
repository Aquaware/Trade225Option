import datetime
import threading
import time as pyTime


def today():
    return datetime.datetime.today()

def yesterday():
    return today() - datetime.timedelta(days= 1)

def tomorrow():
    return today() + datetime.timedelta(days= 1)

class Scheduler():

    def __init__(self, intervalSec, web, loginCallback, closeCallback, callback):
        self.intervalSec = intervalSec
        self.loginCallback = loginCallback
        self.closeCallback = closeCallback
        self.callback = callback
        self.web = web
        self.isStopped = True
        t = threading.Timer(1, self.worker)
        t.start()
        self.counter = 0
        pass

    def shouldWebClose(self):
        now = today()
        if now.hour == 5 and now.minute == 31:
            return True
        if now.hour == 15 and now.minute == 16:
            return True
        return False

    def isActive(self):
        now = today()
        t1 = datetime.datetime(now.year, now.month, now.day, 5, 31)
        t2 = datetime.datetime(now.year, now.month, now.day, 8, 00)
        if now >= t1 and now <= t2:
            return False

        t3 = datetime.datetime(now.year, now.month, now.day, 15, 16)
        t4 = datetime.datetime(now.year, now.month, now.day, 16, 00)
        if now >= t3 and now <= t4:
            return False
        return True

    def worker(self):
        self.counter += 1
        #if self.counter % 100 == 0:
        #    print('now: ', today(), 'begin: ', self.begin, 'end: ', self.end)
        if self.isActive():
            if self.isStopped:
                self.loginCallback()
                self.isStopped = False
            self.callback()

        t = threading.Timer(self.intervalSec, self.worker)
        t.start()
        pass