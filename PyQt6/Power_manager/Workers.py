import os,shutil
import sys
from PyQt6.QtCore import pyqtSignal, QObject

class ScanWorker(QObject):
    finished = pyqtSignal(int, int)

    def __init__(self,Path=None):
        super().__init__()
        self.Path = Path

    def run_scan(self):
        path = self.Path
        dirs = 0
        files = 0

        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_file():
                 files += 1
                if entry.is_dir():
                  dirs += 1

        self.finished.emit(dirs,files)
