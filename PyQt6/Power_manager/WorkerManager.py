from PyQt6.QtCore import QThread
from PyQt6.QtGui import QStandardItem
from PyQt6.QtWidgets import QFileDialog
from Workers import ScanWorker
from itertools import zip_longest

def browse_dirs(self):
    folder = QFileDialog.getExistingDirectory(self, "Select Folder"
                                              , "", QFileDialog.Option.ShowDirsOnly)
    if folder:
        self.folder_path.setText(folder)
        self.folder_path.setReadOnly(False)
        self.scan.setDisabled(False)
        self.extension.setPlaceholderText("Ignore if not...")




class ScanManager:
    def __init__(self,ui):
        self.thread = None
        self.worker = None
        self.ui = ui

    def scan(self,path):
        if path:
           chk_status = (self.ui.chk_files.isChecked(),
                         self.ui.chk_dirs.isChecked(),
                         self.ui.chk_subdirs.isChecked(),
                         self.ui.chk_hidden.isChecked(),
                         self.ui.chk_preview.isChecked())

           self.thread = QThread()
           self.worker = ScanWorker(path=path,chk_status=chk_status)
           self.worker.moveToThread(self.thread)

           self.thread.started.connect(self.worker.run_scan)
           self.worker.finished.connect(self.on_scan_finished)
           self.worker.finished.connect(self.thread.quit)

           self.worker.finished.connect(self.worker.deleteLater)
           self.thread.finished.connect(self.thread.deleteLater)

           self.thread.start()
        else:
            return

    def on_scan_finished(self,*args):
        dirs, files, subdirs,filenames,dirnames= args
        self.ui.dirs_label.setText(f"Folders : {dirs}")
        self.ui.files_label.setText(f"Files : {files}")
        self.ui.subdirs_label.setText(f"Subdirs : {subdirs}")
        print(dirnames)
        if filenames or dirnames:
           model = self.ui.preview_model
           model.clear()
           model.setHorizontalHeaderLabels(["Directories", "Files"])
           for file,dir in zip_longest(filenames,dirnames,fillvalue=QStandardItem("")):
               model.appendRow([dir,file])



