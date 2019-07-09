import pythoncom
import threading
import wx
from main_window import MainWindow

WX_EVT_CUSTOM_ID = wx.NewId()


class MyWxCustomEvent(wx.PyEvent):
    def __init__(self):
        self.event_id = WX_EVT_CUSTOM_ID
        wx.PyEvent.__init__(self)
        self.SetEventType(self.event_id)
        self.message = "I like ice cream"


class Worker(object):
    def __init__(self):
        self.started = False
        self.thread = threading.Thread(target=self.thread_proc)
        self.window_to_publish_to = None

        print "Worker Class created on Id {}".format(threading.current_thread().ident)

    def __del__(self):
        self.stop()

    def start(self):
        if self.started:
            self.stop()

        self.started = True
        self.thread.start()

    def stop(self):
        if not self.started:
            return

        self.started = False
        self.thread.join()

    def thread_proc(self):
        print "Worker thread started with Id {}".format(threading.current_thread().ident)
        while self.started:
            if self.window_to_publish_to:
                custom_event = MyWxCustomEvent()
                wx.PostEvent(self.window_to_publish_to, custom_event)

            pythoncom.PumpWaitingMessages()

        print "Worker thread exiting..."


def main():
    worker = Worker()
    worker.start()

    app = wx.App(False)
    frame = MainWindow(None, 'Two Pumps Testing')
    Worker.window_to_publish_to = frame
    app.MainLoop()

    worker.stop()


if __name__ == "__main__":
    main()
