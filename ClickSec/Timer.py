import datetime
import threading
import time as pyTime


def today():
    return datetime.datetime.today()

def yesterday():
    return today() - datetime.timedelta(days= 1)

def tomorrow():
    return today() + datetime.timedelta(days= 1)


class Timer(threading.Timer):
    def __init__(self, interval, callback, args=[], kwargs={}, multi_thread=False):
        threading.Timer.__init__(self, interval, self.run, args, kwargs)
        self.callback = callback
        self.multi_thread = multi_thread
        self.thread = None
        self.prev_thread = None
        self.stop_signal = False
        self.e = threading.Event()
        self.e.set()

    def run(self):
        #複数実行禁止の場合、event setを待つ
        if(self.multi_thread is False):
            self.e.wait()
            self.e.clear()
        #次スレッド作成（停止信号が来てなければ作成）
        if(self.stop_signal is False):
            self.prev_thread = self.thread
            self.thread=threading.Timer(self.interval, self.run)
            self.thread.start()
            #関数実行
            self.callback()
        #event set
        self.e.set()

    def stop(self):
        self.stop_signal = True
        try:
            if self.thread is not None:
                self.thread.cancel()
                if self.prev_thread != None:
                    self.prev_thread.join()
                    self.thread = None
        except:
            pass