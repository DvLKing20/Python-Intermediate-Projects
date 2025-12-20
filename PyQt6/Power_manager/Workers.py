import os,shutil
import sys
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QStandardItem

class ScanWorker(QObject):
    finished = pyqtSignal(int,int,int,list,list)

    def __init__(self, path: str, chk_status: tuple,) -> None:
        super().__init__()
        self.Path = path

        (self.chk_files_status,
        self.chk_dirs_status,
        self.chk_subdirs_status,
        self.chk_hidden_status,
        self.chk_preview_status) = chk_status

        self.files = self.dirs = self.subdirs = 0
        self.filenames = []
        self.dirnames = []

    def run_scan(self):
        path = self.Path
        try:
          with os.scandir(path) as entries:
            for entry in entries:
               if entry.is_file() and self.chk_files_status:
                  self.files += 1
                  if not self.chk_preview_status:
                     self.filenames.append(QStandardItem(entry.name))

               if entry.is_dir() and self.chk_dirs_status:
                  self.dirs += 1
                  if not self.chk_preview_status:
                     self.dirnames.append(QStandardItem(entry.name))

                  if self.chk_subdirs_status:
                     self.run_subdir_scan(entry.path)


        except OSError as e:
         print(e)

        self.finished.emit(self.dirs,self.files,self.subdirs,self.filenames,self.dirnames)

    def run_subdir_scan(self, path):
        try:
          with os.scandir(path) as entries:
               for entry in entries:
                   if entry.is_file() and self.chk_files_status:
                      self.files += 1
                      if not self.chk_preview_status:
                         self.filenames.append(QStandardItem(entry.name))

                   if entry.is_dir() and self.chk_dirs_status:
                      self.subdirs += 1
                      if not self.chk_preview_status:
                         self.dirnames.append(QStandardItem(entry.name))

                      if self.chk_subdirs_status:
                         self.run_subdir_scan(entry.path)

        except OSError as e:
            print(e)
