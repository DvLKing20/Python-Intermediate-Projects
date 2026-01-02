from PyQt6.QtCore import QThread
from Workers import (ScanWorker,RenameWorker,CreateWorker,CopyWorker)


class ScanJob:
    def __init__(self,manager):
        self.thread = None
        self.worker = None
        self.manager = manager

    def run_thread(self,path,scan_status,extension):
        if path:

           self.thread = QThread()
           self.worker = ScanWorker(path=path,chk_status=scan_status,extension=extension)
           self.worker.moveToThread(self.thread)

           self.thread.started.connect(self.worker.run_scan)
           self.worker.finished.connect(self.on_scan_finished)
           self.worker.finished.connect(self.thread.quit)

           self.worker.finished.connect(self.worker.deleteLater)
           self.thread.finished.connect(self.thread.deleteLater)

           self.thread.start()

    def cancel_thread(self):
        if self.worker:
            self.worker.stop_scan()

    def on_scan_finished(self,*args):
        self.manager.update_table_view(*args)


class RenameJob:
    def __init__(self,manager):
        self.running = False
        self.undo_redo = None
        self.undo_thread = None
        self.thread = None
        self.worker = None
        self.manager = manager

    def run_thread(self,path,text,rename_status,apply):
        if self.running:
           return

        if path:
            self.thread = QThread()
            self.worker = RenameWorker(path=path,chk_status=rename_status,text=text,apply=apply)

            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run_rename)
            self.worker.finished.connect(self.on_rename_finished)
            self.worker.finished.connect(self.thread.quit)

            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
            self.running = True

    def on_rename_finished(self,*args):
        self.manager.update_table_view(*args)
        self.running = False

    def cancel_thread(self):
        if self.running:
           self.worker.stop_rename()

    def run_undo_thread(self,file_stack,dir_stack,state):
        if file_stack or dir_stack:
           self.undo_redo = RenameWorker.UndoRedo(file_stack,dir_stack,state)
           self.undo_thread = QThread()

           self.undo_redo.moveToThread(self.undo_thread)
           self.undo_thread.started.connect(self.undo_redo.main)
           self.undo_redo.finished.connect(self.undo_state)
           self.undo_redo.finished.connect(self.undo_thread.quit)

           self.undo_redo.finished.connect(self.undo_redo.deleteLater)
           self.undo_thread.finished.connect(self.undo_thread.deleteLater)

           self.undo_thread.start()

    def undo_state(self,*args):
        self.manager.refresh_undo(*args)

class CreateJob:
    def __init__(self,manager):
        self.thread = None
        self.worker = None
        self.manager = manager

    def run_thread(self,path,file_name,ext,count,mode,apply,folder_name="",state=None):
        if path:
           self.worker = CreateWorker(path,file_name,folder_name,ext,count,mode,state,apply)
           self.thread = QThread()
           self.worker.moveToThread(self.thread)
           self.thread.started.connect(self.worker.run_create)
           self.worker.finished.connect(self.on_create_finished)
           self.worker.finished.connect(self.thread.quit)

           self.thread.finished.connect(self.thread.deleteLater)
           self.worker.finished.connect(self.worker.deleteLater)

           self.thread.start()

    def on_create_finished(self,*args):
        self.manager.update_table_view(*args)

    def cancel_thread(self):
        if not self.worker:
            return
        self.worker.running = False

class CopyJob:
    def __init__(self,manager):
        self.thread = None
        self.worker = None
        self.manager = manager

    def run_thread(self,src_path,dst_path,scope,copy_mode,collision,count,apply):
        if src_path and dst_path:
            self.worker = CopyWorker(src_path, dst_path, scope, copy_mode, collision, count, apply)
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.main)
            self.worker.finished.connect(self.on_copy_finished)
            self.worker.finished.connect(self.thread.quit)

            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.finished.connect(self.worker.deleteLater)

            self.thread.start()

    def cancel_thread(self):
        if not self.worker:
           return
        self.worker.running = False

    def on_copy_finished(self,*args):
        self.manager.update_table_view(*args)