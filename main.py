import pythoncom
import threading
import wx
from main_window import MainWindow


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
            pythoncom.PumpWaitingMessages()

        print "Worker thread exiting..."


def main():
    worker = Worker()
    worker.start()

    app = wx.App(False)
    frame = MainWindow(None, 'Two Pumps Testing')
    app.MainLoop()

    worker.stop()


if __name__ == "__main__":
    main()
