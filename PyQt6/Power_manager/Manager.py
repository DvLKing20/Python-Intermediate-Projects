from PyQt6.QtCore import QTimer, QDir, QSize
from PyQt6.QtGui import QStandardItem, QFileSystemModel, QIcon
from itertools import zip_longest
from PyQt6.QtWidgets import QTreeView, QVBoxLayout
from states import (ScanMode,RenameState,UndoState,CreateState,CopyState)
from Job import (ScanJob,RenameJob,CreateJob,CopyJob)
from style import VIEW_STYLE

class BrowseDir:
    def __init__(self, ui):
        self.ui = ui
        self.view = QTreeView()
        self.model = QFileSystemModel()

    def browse_dirs(self):
        browser = self.ui.browser
        browser.resize(600,500)
        browser.setWindowTitle("Browse Directory")
        browser.setWindowIcon(QIcon("f.jpeg"))

        self.model.setRootPath(QDir.rootPath())
        self.view.setModel(self.model)
        self.view.doubleClicked.connect(self.on_double_click)

        self.view.setStyleSheet(VIEW_STYLE)
        self.view.setColumnWidth(0, 260)  # Name
        self.view.setColumnWidth(1, 100)  # Size
        self.view.setColumnWidth(2, 120)  # Type
        self.view.setColumnWidth(3, 180)  # Date Modified

        self.view.header().setStyleSheet("""
             QHeaderView::section {
                 padding-left: 12px;
                 padding-right: 12px;
                 padding-top: 6px;
                 padding-bottom: 6px;
             }
        """)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.ui.browser.setLayout(layout)
        browser.show()

    def on_double_click(self, index):
        selected = self.model.filePath(index)
        self.ui.folder_path.setText(str(selected))
        self.ui.scan.setDisabled(False)
        self.ui.browser.hide()

class ScanManager:
    """Allocates a new thread for scanning and intializes the ScanWorker class to run the code."""
    def __init__(self,ui):
        self.scan_mode = ScanMode.SCAN
        self.scan_job = ScanJob(self)
        self.ui = ui

    def update_button(self):
        button = self.ui.scan
        match self.scan_mode:
            case ScanMode.SCAN:
                button.setText("SCAN")
            case ScanMode.STOP:
                button.setText("STOP?")

    def scan(self):
        self.ui.scan_bar.show()
        path = self.ui.folder_path.text()
        extension = self.ui.scan_input.text()
        scan_status = [checks.isChecked() for checks in self.ui.scan_checks.values()]

        match self.scan_mode:
            case ScanMode.SCAN:
                 self.scan_mode = ScanMode.STOP
                 self.update_button()
                 self.scan_job.run_thread(path,scan_status,extension)
            case ScanMode.STOP:
                 self.ui.scan_bar.hide()
                 self.ui.scan.setDisabled(True)
                 self.scan_job.cancel_thread()

    def update_table_view(self,dirs, files, subdirs, filenames, dirnames):
        self.ui.preview_model.clear()
        self.ui.scan.setDisabled(False)
        updated_labels = (f"Files : {files}",
                          f"Folders : {dirs}",
                          f"SubFolders : {subdirs}")

        for idx,label in enumerate(updated_labels):
            self.ui.scan_labels[idx].setText(label)

        if filenames or dirnames:
           model = self.ui.preview_model
           preview = self.ui.preview_table
           model.clear()
           model.setHorizontalHeaderLabels(["Directories", "Files"])
           preview.setColumnWidth(0, 350)
           for file,dir in zip_longest(filenames,dirnames,fillvalue=""):
               model.appendRow([QStandardItem(dir),QStandardItem(file)])
        self.ui.scan_bar.hide()
        self.scan_mode = ScanMode.SCAN
        self.update_button()
        self.ui.scan.setDisabled(False)

class RenameManager:
    def __init__(self,ui):
        self.rename_mode = RenameState.APPLY
        self.undo_mode = UndoState.UNDO
        self.rename_job = RenameJob(self)

        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.run_live_preview)
        self.ui = ui
        self.file_stack = None
        self.dir_stack = None

    def on_rename_mode_changed(self):
        rename_input = self.ui.rename_input
        state = tuple([check.isChecked() for check in self.ui.rename_scope])

        preview_enabled = self.ui.rename_checks["preview"].isChecked()
        rename_input.setEnabled(state != (False, False, True, False))
        self.ui.rename_label.setText("Specific Extension: ?"
                                     if state == (False, False, False, True)
                                     else "Specific Name: ?")
        self.rename_mode = (
            RenameState.PREVIEW if preview_enabled
            else RenameState.APPLY
        )
        self.update_button()

    def update_button(self):
        button = self.ui.rename
        undo = self.ui.undo

        match self.rename_mode:
            case RenameState.PREVIEW:
                button.setText("Preview")
            case RenameState.APPLY:
                button.setText("Apply")
            case RenameState.CANCEL:
                button.setText("Cancel?")

        match self.undo_mode:
            case UndoState.UNDO:
                undo.setText("Undo")
            case UndoState.REDO:
                undo.setText("Redo")

    def get_case_mode(self,active,checks):
        for check in checks:
            if check is not active:
                check.blockSignals(True)
                check.setChecked(False)
                check.blockSignals(False)

    def rename(self):
        rename_text = self.ui.rename_input.text()
        path = self.ui.folder_path.text()
        self.ui.undo.hide()
        rename_status = (tuple([btn.isChecked() for btn in self.ui.rename_scope]),
                         tuple([check.isChecked() for check in self.ui.rename_checks.values()]),
                         tuple([case.isChecked() for case in self.ui.cases]))
        if not path:
           return
        match self.rename_mode:
            case RenameState.PREVIEW:
                 self.rename_job.run_thread(path,rename_text,rename_status,apply=False)
            case RenameState.APPLY:
                 self.rename_mode = RenameState.CANCEL
                 self.update_button()
                 self.ui.rename_bar.show()
                 self.rename_job.run_thread(path,rename_text,rename_status,apply=True)
            case RenameState.CANCEL:
                 self.rename_job.cancel_thread()

    def on_text_changed(self,_):
        if self.rename_job.running:
           self.rename_job.cancel_thread()

        if not self.ui.rename_checks["live_preview"].isChecked():
           return
        self.ui.undo.hide()
        # Restart timer on every keystroke
        self.preview_timer.start(300)

    def run_live_preview(self):
        self.ui.rename_bar.show()
        self.rename_mode = RenameState.PREVIEW
        self.ui.rename.setDisabled(True)
        self.rename()
        self.rename_mode = RenameState.APPLY
        self.ui.rename.setEnabled(True)

    def update_table_view(self,source_files,target_files,source_dirs,target_dirs,file_stack,dir_stack,did_apply):
        model = self.ui.preview_model
        preview = self.ui.preview_table
        if file_stack or dir_stack:
           self.file_stack = tuple(file_stack)
           self.dir_stack = tuple(dir_stack)

        def setup_columns(headers, widths, model, preview):
            model.setHorizontalHeaderLabels(headers)
            for i, w in enumerate(widths):
                preview.setColumnWidth(i, w)

        model.clear()
        if source_files and source_dirs:
            headers = ["Original Folder","Original Files",
                       "Preview Folder", "Preview Files"]
            widths = (200,200,200,200)
            setup_columns(headers,widths,model,preview)
            rows = zip_longest(
                source_dirs, source_files,
                target_dirs, target_files,
                fillvalue=""
            )
            for od, of, rd, rf in rows:
                model.appendRow([
                    QStandardItem(od), QStandardItem(of),
                    QStandardItem(rd), QStandardItem(rf)
                ])
        elif source_files or source_dirs:
             if source_files:
                model.setHorizontalHeaderLabels(["Original Files", "Preview"])
                preview.setColumnWidth(0, 350)
                for org_file, re_file in zip(source_files, target_files):
                    model.appendRow([QStandardItem(org_file), QStandardItem(re_file)])
             else:
                 model.setHorizontalHeaderLabels(["Original Folder", "Preview"])
                 preview.setColumnWidth(0, 350)
                 for org_dir, re_dir in zip(source_dirs, target_dirs):
                     model.appendRow([QStandardItem(org_dir), QStandardItem(re_dir)])

        if did_apply:
           self.undo_mode = UndoState.UNDO
           self.rename_mode = RenameState.APPLY
           self.update_button()
           self.ui.rename_bar.hide()
           self.ui.undo.show()
        else:
            self.ui.rename_bar.hide()

    def on_cick_undo(self):
        if self.file_stack or self.dir_stack:
           self.rename_job.run_undo_thread(self.file_stack,self.dir_stack,self.undo_mode)

    def refresh_undo(self,old_file,new_file,old_dir,new_dir,state):
        self.ui.undo.setDisabled(True)
        self.update_table_view(old_file,new_file,old_dir,new_dir,False,False,False)
        self.undo_mode = state
        self.update_button()
        self.ui.undo.setEnabled(True)


class CreateManager:
    def __init__(self,ui):
        self.ui = ui
        self.create_mode = CreateState.ModeState.SIMPLE
        self.button_mode = CreateState.ButtonState.PREVIEW
        self.create_job = CreateJob(self)

    def on_create_mode_changed(self):
        state = ([state.isChecked() for state in self.ui.create_mode.values()])
        modes = self.ui.create_mode
        match state:
              case (True,False):
                   self.create_mode = CreateState.ModeState.SIMPLE
                   modes["simple"].hide()
                   modes["custom"].show()
                   self.ui.create_stack.setCurrentIndex(0)
              case _:
                   self.create_mode = CreateState.ModeState.CUSTOM
                   modes["custom"].hide()
                   modes["simple"].show()
                   self.ui.create_stack.setCurrentIndex(1)

    def on_simple_mode_changed(self):
        simple_mode = ([state.isChecked() for state in self.ui.create_simple_mode])
        simple_input = self.ui.create_simple_input
        match simple_mode:
              case (False,True):
                   simple_input["name"].setPlaceholderText("Enter the folder name you like give...")
                   simple_input["ext"].setDisabled(True)
              case _:
                   simple_input["name"].setPlaceholderText("Enter the file name you like give...")
                   simple_input["ext"].setEnabled(True)


    def update_button(self):
        button = self.ui.create

        match self.button_mode:
            case CreateState.ButtonState.PREVIEW:
                button.setText("Preview")
            case CreateState.ButtonState.CREATE:
                button.setText("Generate")
            case CreateState.ButtonState.CANCEL:
                button.setText("Cancel")

    def on_checkbox_toggled(self,state: bool):
        match state:
              case True:
                  self.button_mode = CreateState.ButtonState.PREVIEW
              case _:
                  self.button_mode = CreateState.ButtonState.CREATE

        self.update_button()

    def create(self):
        simple_input = self.ui.create_simple_input
        custom_input = self.ui.create_custom_input
        button = self.ui.create

        path = self.ui.folder_path.text()
        thread = self.create_job.run_thread
        apply = False
        if not path:
            return
        match self.button_mode:
            case CreateState.ButtonState.PREVIEW:
                 apply = False
            case CreateState.ButtonState.CREATE:
                 self.button_mode = CreateState.ButtonState.CANCEL
                 apply = True
            case CreateState.ButtonState.CANCEL:
                 self.button_mode = CreateState.ButtonState.CREATE
                 button.setDisabled(True)
                 self.create_job.cancel_thread()

        match self.create_mode:
              case CreateState.ModeState.SIMPLE:
                   base_name = simple_input["name"].text()
                   ext = simple_input["ext"].text()
                   count = self.ui.create_simple_spin.value()
                   state = ([state.isChecked() for state in self.ui.create_simple_mode])
                   mode = self.create_mode
                   thread(path,base_name,ext,count,mode,apply,state=state)

              case CreateState.ModeState.CUSTOM:
                   file_name = custom_input["file"].text()
                   folder_name = custom_input["folder"].text()
                   ext = custom_input["ext"].text()
                   counts = {}
                   for key,count in self.ui.create_custom_combo.items():
                       counts[key] = int(count.currentText())
                   mode = self.create_mode
                   thread(path,file_name,ext,counts,mode,apply,folder_name=folder_name)

        self.update_button()

    def update_table_view(self,files,folders,mode,did_apply):
        model = self.ui.preview_model
        table = self.ui.preview_table
        model.clear()
        match mode:
              case CreateState.ModeState.SIMPLE:
                   items = files if files else folders
                   header = ("Files" if files else "Folders")
                   table.setColumnWidth(0, 350)
                   model.setHorizontalHeaderLabels([header])
                   for item in items:
                       model.appendRow([QStandardItem(item)])

              case CreateState.ModeState.CUSTOM:
                   header = ("Directories", "Files")
                   model.setHorizontalHeaderLabels(header)
                   table.setColumnWidth(0, 350)
                   for file, folder in zip_longest(files, folders, fillvalue=""):
                       model.appendRow([QStandardItem(folder), QStandardItem(file)])
        self.running = False
        if did_apply:
           self.button_mode = CreateState.ButtonState.CREATE
           self.update_button()


class CopyManager:
    def __init__(self,ui):
        self.ui = ui
        self.button_mode = CopyState.ButtonState.PREVIEW
        self.copy_job = CopyJob(self)

    def update_button(self):
        button = self.ui.copy
        match self.button_mode:
            case CopyState.ButtonState.PREVIEW:
                 button.setText("Preview")
            case CopyState.ButtonState.COPY:
                 button.setText("Copy")
            case CopyState.ButtonState.CANCEL:
                 button.setText("CANCEL")

    def on_clicked_copy_mode(self,label):
        mode = ([mode.isChecked() for mode in self.ui.copy_mode.values()])
        spin = self.ui.copy_spin

        match mode:
            case (False,True,False):
                label.show()
                spin.setEnabled(True)
                spin.show()
            case _:
                label.hide()
                spin.setDisabled(True)
                spin.hide()

    def on_clicked_button_mode(self):
        bar = self.ui.copy_bar
        button = self.ui.copy
        src_path = self.ui.folder_path.text()
        dst_path = self.ui.copy_dst.text()
        if not src_path and not dst_path:
           return

        CANCEL = False
        apply = False
        thread = self.copy_job.run_thread
        match self.button_mode:
              case CopyState.ButtonState.PREVIEW:
                   apply = False
                   self.button_mode = CopyState.ButtonState.COPY
              case CopyState.ButtonState.COPY:
                   bar.show()
                   apply = True
                   self.button_mode = CopyState.ButtonState.CANCEL
              case CopyState.ButtonState.CANCEL:
                   CANCEL = True
                   button.setDisabled(True)
                   self.button_mode = CopyState.ButtonState.PREVIEW
                   self.copy_job.cancel_thread()
        self.update_button()

        scope = ([scope.isChecked() for scope in self.ui.copy_scope.values()])
        copy_mode = ([mode.isChecked() for mode in self.ui.copy_mode.values()])
        collisions = ([c.isChecked() for c in self.ui.copy_collison.values()])
        count = self.ui.copy_spin.value()

        if CANCEL:
           CANCEL = False
           return
        thread(src_path,dst_path,scope,copy_mode,collisions,count,apply)

    def update_table_view(self,files,folders,did_apply):
        button = self.ui.copy
        model = self.ui.preview_model
        table = self.ui.preview_table
        model.clear()

        if files and folders:
             header = ("Directories", "Files")
             model.setHorizontalHeaderLabels(header)
             table.setColumnWidth(0, 350)
             for file, folder in zip_longest(files, folders, fillvalue=""):
                 model.appendRow([QStandardItem(folder), QStandardItem(file)])

        elif files or folders:
            items = files if files else folders
            header = ("Files" if files else "Folders")
            model.setHorizontalHeaderLabels([header])
            for item in items:
                    model.appendRow([QStandardItem(item)])

        if did_apply:
            button.setEnabled(True)
            self.ui.copy_bar.hide()
            self.button_mode = CopyState.ButtonState.PREVIEW
            self.update_button()