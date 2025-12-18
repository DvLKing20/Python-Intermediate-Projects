from PyQt6.QtCore import QThread
from Workers import ScanWorker


class ScanManager:
    def __init__(self,ui):
        self.thread = None
        self.worker = None
        self.forward = ui

    def scan(self,path):
        if path:
           self.thread = QThread()
           self.worker = ScanWorker(path)
           self.worker.moveToThread(self.thread)

           self.thread.started.connect(self.worker.run_scan)
           self.worker.finished.connect(self.on_scan_finished)
           self.worker.finished.connect(self.thread.quit)

           self.thread.start()
        else:
            self.on_scan_finished(0,0,0)

    def on_scan_finished(self,dirs,files,subdirs):
        self.forward.update_scanned_counts(dirs,files,subdirs)