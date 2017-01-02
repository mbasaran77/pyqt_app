

from threading import Timer

import time



class repetedTimer():

    def __init__(self,interval,function,*args,**kwargs):
        self._timer=None
        self.interval=interval
        self.function=function
        self.args=args
        self.kwargs=kwargs
        self.is_running=False
        self.start()

    def _run(self):
        self.is_running=False
        self.start()
        self.function(*self.args,**self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer=Timer(self.interval,self._run)
            self._timer.start()
            self.is_running=True

    def stop(self):
        self._timer.cancel()
        self.is_running=False



def hello(name):
    print("Hello %s"%name)
    time.sleep(1)
    print("güle güle")

print("starting..............")

rt=repetedTimer(3,hello,"ramazan")
try:
    time.sleep(12)
finally:
    rt.stop()

print("bitti....")