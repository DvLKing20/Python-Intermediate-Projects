from PyQt6.QtGui import QIcon, QPainter,QStandardItemModel,QFont
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
, QLabel, QLineEdit, QStackedLayout, QGraphicsView, QRadioButton,
                             QGraphicsScene, QStackedWidget,
                             QButtonGroup, QTableView, QToolButton, QSizePolicy, QCheckBox, QGroupBox, QHeaderView,
                             QProgressBar, QComboBox, QSpinBox, QFileDialog)
from PyQt6.QtCore import Qt, QSizeF, QUrl
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
import sys

import Manager
from style import STYLE


BASE_FONT_SIZE = 13
BASE_DPI = 102

class PowerManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.structure_widget = None
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

        #PREVIEW TABLE
        self.preview_table = QTableView()
        self.preview_model = QStandardItemModel(0, 1)

        #TOOL BUTTONS
        self.btn_scan = QToolButton()
        self.btn_rename = QToolButton()
        self.btn_create = QToolButton()
        self.btn_copy = QToolButton()
        self.mode_group = QButtonGroup()

        #WIDGETS
        self.browser = QWidget()
        self.central_widget = QWidget()
        self.screen_widget = QWidget()
        self.stacked_widget = QStackedWidget()
        self.create_stack = QStackedWidget()
        self.browse_widget = QWidget()
        self.mode_widget = QWidget()
        self.container = QWidget()
        self.wrapper_panels = QWidget()
        self.scope_wrapped = QWidget()
        self.chk_widget = QWidget()

        #Graphics Item
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.video_item = QGraphicsVideoItem()

        #LABELS
        self.scan_labels = (QLabel("Folders : 0"),
                           QLabel("Files : 0"),
                           QLabel("Subdirs : 0"),)
        self.scan_label = QLabel("Specific Extension: ?")
        self.rename_label = QLabel("Specific Name: ?")

        #LINE EDITS
        self.folder_path = QLineEdit()
        self.scan_input = QLineEdit()
        self.rename_input = QLineEdit()
        self.create_simple_input = {"name": QLineEdit(),
                                    "ext": QLineEdit()}

        self.create_custom_input = {"file": QLineEdit(),
                                    "folder": QLineEdit(),
                                    "ext": QLineEdit()}

        self.copy_dst = QLineEdit()

        #SPINBOX
        self.create_simple_spin = QSpinBox()
        self.copy_spin = QSpinBox()

        #COMBOBOX
        self.create_custom_combo =  {"file": QComboBox(),
                              "folder": QComboBox(),
                              "depth": QComboBox()}

        #CHECKBOXES
        self.cases = (QCheckBox("Capitalize"),
                      QCheckBox("Uppercase"),
                      QCheckBox("Lowercase"),
                      QCheckBox("Title Case"))
        self.copy_scope = None

        #PUSH BUTTONS
        self.browse = QPushButton("📂")
        self.scan = QPushButton("SCAN")
        self.rename = QPushButton("Apply")
        self.shortcut_rename = QPushButton("RMShortcut")
        self.undo = QPushButton("Undo")
        self.create = QPushButton("Create")
        self.copy = QPushButton("Copy")

        #RADIO BUTTON
        self.rename_scope = (QRadioButton("Prefix."),
                          QRadioButton("Suffix."),
                          QRadioButton("Sequence."),
                          QRadioButton("Ext."))

        self.create_simple_mode = (QRadioButton("Files."),
                                   QRadioButton("Folder."))

        self.create_mode = {"simple": QRadioButton("Simple."),
                             "custom": QRadioButton("Custom.")}

        self.copy_collison = None

        #progress Bar
        self.scan_bar = QProgressBar()
        self.rename_bar = QProgressBar()
        self.create_bar =  QProgressBar()
        self.copy_bar = QProgressBar()

        #WorkerClasses
        self.browse_dir = Manager.BrowseDir(self)
        self.scanner = Manager.ScanManager(self)
        self.renamer = Manager.RenameManager(self)
        self.creater = Manager.CreateManager(self)
        self.copier = Manager.CopyManager(self)

        #UI
        self.init_ui()

        #TOOL BUTTON CONNECTIONS
        self.mode_group.idClicked.connect(self.stacked_widget.setCurrentIndex)

        #CONNECTIONS
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.browse.clicked.connect(self.browse_dir.browse_dirs)
        self.scan.clicked.connect(self.scanner.scan)
        self.rename.clicked.connect(self.renamer.rename)
        self.undo.clicked.connect(self.renamer.on_cick_undo)
        self.rename_input.textChanged.connect(self.renamer.on_text_changed)
        self.create.clicked.connect(self.creater.create)
        self.copy.clicked.connect(self.copier.on_clicked_button_mode)

        for btn in self.rename_scope:
            btn.toggled.connect(self.renamer.on_rename_mode_changed)

        for chk in self.cases:
            chk.toggled.connect(lambda _,active=chk,checks=self.cases: self.renamer.get_case_mode(active,checks))

        for btn in self.create_mode.values():
            btn.toggled.connect(self.creater.on_create_mode_changed)

        for btn in self.create_simple_mode:
            btn.toggled.connect(self.creater.on_simple_mode_changed)


    @staticmethod
    def build_scope_checkboxes(group_box: QGroupBox):
        layout = QVBoxLayout(group_box)
        layout.setContentsMargins(5, 5, 5, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        boxes = {
            "files": QCheckBox("Files", group_box),
            "dirs": QCheckBox("Folders", group_box),
            "subdirs": QCheckBox("SubFolders", group_box),
            "preview": QCheckBox("No Preview", group_box),
            "hidden": QCheckBox("Hidden Files", group_box),
        }
        group_box.setSizePolicy(QSizePolicy.Policy.Expanding,
                                QSizePolicy.Policy.Expanding)
        for box in boxes.values():
            layout.addWidget(box)

        return boxes

    @staticmethod
    def set_scaled_font():
        app = QApplication.instance()
        if not app:
            return app

        screen = app.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        scale =  dpi / BASE_DPI

        font = QFont()
        font.setPointSizeF(BASE_FONT_SIZE * scale)
        app.setFont(font)

    def resizeEvent(self,event):
         super().resizeEvent(event)

         new_width = self.central_widget.width()
         new_height = self.central_widget.height()

         #VIDEO ITEM
         self.scene.setSceneRect(0,0,new_width,new_height)
         self.video_item.setSize(QSizeF(new_width,new_height))

         #mode buttons
         self.mode_widget.setMaximumSize(int(new_width*0.80),int(new_height*0.085))

         #BROWSE AREA
         self.browse_widget.setMaximumSize(int(new_width*0.43),int(new_height*0.092))
         self.browse.setMaximumSize(int(new_width*0.050),int(new_height*0.090))

         self.container.setMaximumWidth(int(new_width * 0.324))


    def init_ui(self):

       #WINDOW:
        self.setWindowTitle("Made By DvLKing20")
        self.setWindowIcon(QIcon("f.jpeg"))
        self.resize(1200,620)

       #TOP BUTTONS:
        self.btn_scan.setText("SCAN")
        self.btn_rename.setText("RENAME")
        self.btn_create.setText("CREATE")
        self.btn_copy.setText("COPY")
        self.mode_group.setExclusive(True)

        self.mode_group.addButton(self.btn_scan, 0)
        self.mode_group.addButton(self.btn_rename, 1)
        self.mode_group.addButton(self.btn_create, 2)
        self.mode_group.addButton(self.btn_copy, 3)
        self.btn_scan.setChecked(True)

        mode_simple = QHBoxLayout(self.mode_widget)
        mode_simple.setSpacing(0)
        mode_simple.addWidget(self.btn_scan)
        mode_simple.addWidget(self.btn_rename)
        mode_simple.addWidget(self.btn_create)
        mode_simple.addWidget(self.btn_copy)
        mode_simple.addStretch()
        self.mode_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        for btn in (
            self.btn_scan,
            self.btn_rename,
            self.btn_copy,
            self.btn_create,
        ):
           btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
           btn.setCheckable(True)
           btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
           btn.setCursor(Qt.CursorShape.PointingHandCursor)

       #BROWSE PANEL:
        self.folder_path.setPlaceholderText("Choose a folder...")
        self.browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo.hide()

        browse_layout = QHBoxLayout(self.browse_widget)
        browse_layout.setSpacing(5)
        browse_layout.setContentsMargins(10, 10, 10, 10)
        browse_layout.addWidget(self.folder_path)
        browse_layout.addWidget(self.browse)
        browse_layout.addSpacing(50)
        browse_layout.addWidget(self.undo)
        self.folder_path.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.browse.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.browse_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

       #SCAN PANEL:
        self.scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_input.setPlaceholderText("Choose a folder first...")
        self.scan.setDisabled(True)
        self.scan_bar.setRange(0, 0)
        self.scan_bar.hide()

        scan_widget = QWidget()
        scan_layout = QHBoxLayout(scan_widget)
        scan_layout.setContentsMargins(5,5,5,5)
        scan_layout.setSpacing(5)
        scan_layout.addWidget(self.scan_input)
        scan_layout.addWidget(self.scan)

        scan_box = QGroupBox("Scan scope")
        self.scan_checks = self.build_scope_checkboxes(scan_box)
        self.scan_checks["files"].setChecked(True)
        self.scan_checks["dirs"].setChecked(True)

        label_widget = QGroupBox("Result")
        label_layout = QVBoxLayout(label_widget)
        label_layout.setSpacing(10)
        for label in self.scan_labels:
            label_layout.addWidget(label)
            label.setSizePolicy(QSizePolicy.Policy.Expanding,
                                QSizePolicy.Policy.Expanding)
        label_widget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)

        scope_box_label_layout = QHBoxLayout(self.scope_wrapped)
        scope_box_label_layout.setSpacing(5)
        scope_box_label_layout.setContentsMargins(0,0,0,0)
        scope_box_label_layout.addWidget(scan_box)
        scope_box_label_layout.addWidget(label_widget)
        self.scope_wrapped.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)

        bar_widget = QWidget()
        bar_layout = QHBoxLayout(bar_widget)
        bar_layout.setContentsMargins(35,5,5,5)
        bar_layout.addWidget(self.scan_bar)
        bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Fixed)

        scan_panel = QWidget()
        scan_panel_layout = QVBoxLayout(scan_panel)
        scan_panel_layout.setContentsMargins(0,0,0,0)
        scan_panel_layout.setSpacing(0)
        scan_panel_layout.addWidget(self.scan_label)
        scan_panel_layout.addWidget(scan_widget)
        scan_panel_layout.addWidget(bar_widget)
        scan_panel_layout.addWidget(self.scope_wrapped)
        scan_panel_layout.addStretch()

       #RENAME PANEL:
        self.rename.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rename_input.setPlaceholderText("What would you like to do?")
        self.rename_scope[0].setChecked(True)
        self.rename_bar.setRange(0, 0)
        self.rename_bar.hide()

        horizontal_widget = QWidget()
        horizontal_layout = QHBoxLayout(horizontal_widget)
        horizontal_layout.setContentsMargins(5,5,5,5)
        horizontal_layout.setSpacing(5)
        horizontal_layout.addWidget(self.rename_input)
        horizontal_layout.addWidget(self.rename)

        radio_button_group = QGroupBox("Scope")
        radio_button_layout = QHBoxLayout(radio_button_group)
        radio_button_layout.setContentsMargins(5,5,5,5)
        radio_button_layout.setSpacing(5)
        for btn in self.rename_scope:
            radio_button_layout.addWidget(btn)

        bar_widget = QWidget()
        bar_layout = QHBoxLayout(bar_widget)
        bar_layout.setContentsMargins(35, 5, 5, 5)
        bar_layout.addWidget(self.rename_bar)
        bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.cases_group = QGroupBox("Cases")
        chk_layout = QVBoxLayout(self.cases_group)
        chk_layout.setContentsMargins(5,5,5,10)
        chk_layout.setSpacing(4)

        for chk in self.cases:
            chk_layout.addWidget(chk)
        chk_layout.addStretch()

        rename_mode = QGroupBox("Convention")
        self.rename_checks = self.build_scope_checkboxes(rename_mode)
        self.rename_checks["files"].setChecked(True)
        p1 = self.rename_checks["live_preview"] = self.rename_checks.pop("preview")
        p2 = self.rename_checks["preview"] = self.rename_checks.pop("hidden")
        p2.setText("Preview")
        p1.setText("Live Preview")
        p1.setChecked(True)
        checks = (p1,p2)
        for p in checks:
            p.toggled.connect(lambda _,active=p,box=checks: self.renamer.get_case_mode(active,box))
            p.toggled.connect(self.renamer.on_rename_mode_changed)


        rename_panel = QWidget()
        rename_panel_layout = QVBoxLayout(rename_panel)
        rename_panel_layout.setContentsMargins(0,0,0,0)
        rename_panel_layout.setSpacing(0)
        rename_panel_layout.addWidget(self.rename_label)
        rename_panel_layout.addWidget(horizontal_widget)
        rename_panel_layout.addWidget(radio_button_group)
        rename_panel_layout.addWidget(bar_widget)
        rename_panel_layout.addWidget(rename_mode)
        rename_panel_layout.addWidget(self.cases_group)
        rename_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

       #CREATE PANEL
        self.create.setText("Preview")
        create_scope = QWidget()
        group_layout = QHBoxLayout(create_scope)
        group_layout.setContentsMargins(0,0,0,0)
        group_layout.setSpacing(0)
        self.create_mode["simple"].hide()
        for btn in self.create_mode.values():
            group_layout.addWidget(btn)
        group_layout.addStretch()

        for box in self.create_custom_combo.values():
            box.clear()
            box.addItems([str(i) for i in range(11)])
            box.setCurrentIndex(0)

        def make_row(label_text, lineedit):
            row = QWidget()
            layout = QHBoxLayout(row)
            layout.setSpacing(3)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.addWidget(QLabel(label_text))
            layout.addWidget(lineedit)
            return row

        custom_widgets = []
        labels = ("File:       ","Folder:    ","Extension:")
        for line,label in zip(self.create_custom_input.values(),labels):
           custom_widgets.append(make_row(label,line))

        self.create_custom_input["file"].setPlaceholderText("Enter file name...")
        self.create_custom_input["folder"].setPlaceholderText("Enter folder name...")
        self.create_custom_input["ext"].setPlaceholderText("Enter file extension...")

        combo_row = QWidget()
        combo_layout = QHBoxLayout(combo_row)
        combo_layout.setSpacing(1)
        combo_layout.setContentsMargins(5,5,5,5)
        for text, combo in self.create_custom_combo.items():
            combo_layout.addWidget(QLabel(text))
            combo_layout.addWidget(combo)
        combo_layout.addStretch()

        simple_mode = QWidget()
        mode_simple = QHBoxLayout(simple_mode)
        mode_simple.setContentsMargins(5, 5, 5, 5)
        mode_simple.setSpacing(0)
        for btn in self.create_simple_mode:
            mode_simple.addWidget(btn)
        mode_simple.addStretch()

        simple_labels = ("Base Name:",
                         "Extension:  ")

        self.create_simple_input["name"].setPlaceholderText("What name you like to give?")
        self.create_simple_input["ext"].setPlaceholderText("What extension you like to use?")
        self.create_simple_mode[0].setChecked(True)
        self.create_simple_spin.setRange(1,1000)
        self.create_simple_spin.setValue(0)

        simple_spin = QWidget()
        spin_layout = QHBoxLayout(simple_spin)
        spin_layout.setContentsMargins(5,5,5,5)
        spin_layout.setSpacing(5)
        spin_layout.addStretch()
        spin_layout.addWidget(QLabel("How Many :"))
        spin_layout.addWidget(self.create_simple_spin)

        simple_row = []
        for label,line in zip(simple_labels,self.create_simple_input.values()):
            simple_row.append(make_row(label,line))

        mode_1 = QGroupBox("Simple Mode")
        mode_simple = QVBoxLayout(mode_1)
        mode_simple.setContentsMargins(5,5,5,5)
        mode_simple.setSpacing(10)
        mode_simple.addWidget(simple_mode)
        for widget in simple_row:
            mode_simple.addWidget(widget)
        mode_simple.addWidget(simple_spin)
        mode_simple.addStretch()

        mode_2 = QGroupBox("Custom Mode")
        mode_custom = QVBoxLayout(mode_2)
        mode_custom.setContentsMargins(5,5,5,5)
        mode_custom.setSpacing(3)
        for widget in custom_widgets:
            mode_custom.addWidget(widget)
        mode_custom.addWidget(combo_row)
        mode_custom.addStretch()

        self.create_stack.addWidget(mode_1)
        self.create_stack.addWidget(mode_2)
        self.create_stack.setCurrentIndex(0)

        chk_preview = QCheckBox("Preview")
        chk_preview.setChecked(True)
        chk_preview.toggled.connect(lambda checked: self.creater.on_checkbox_toggled(checked))

        create_panel = QWidget()
        create_panel_layout = QVBoxLayout(create_panel)
        create_panel_layout.setContentsMargins(0,0,0,0)
        create_panel_layout.setSpacing(0)
        create_panel_layout.addWidget(self.create_stack)
        create_panel_layout.addWidget(chk_preview)
        create_panel_layout.addWidget(self.create,alignment=Qt.AlignmentFlag.AlignRight)
        create_panel_layout.addWidget(create_scope,alignment=Qt.AlignmentFlag.AlignLeft)

       #COPY PANEL
        def create_copy_widget():
           copy_widget = QWidget()
           layout = QVBoxLayout(copy_widget)
           layout.setContentsMargins(5,0,5,10)
           layout.setSpacing(5)
           # ---------------- PATHS ----------------
           paths_group = QGroupBox("Paths")
           paths_layout = QVBoxLayout(paths_group)

           dst_row = QHBoxLayout()
           dst_btn = QPushButton("📂")
           self.copy_dst.setReadOnly(True)
           self.copy_dst.setPlaceholderText("Destination path")
           dst_row.addWidget(self.copy_dst)
           dst_row.addWidget(dst_btn)

           dst_btn.clicked.connect(lambda _:
          (path := QFileDialog.getExistingDirectory(self, "Select Folder"))
           and self.copy_dst.setText(path))

           paths_layout.addLayout(dst_row)

           layout.addWidget(paths_group)

           # ---------------- SCOPE ----------------
           scope_group = QGroupBox("What to copy")
           scope_layout = QHBoxLayout(scope_group)
           scope_layout.setContentsMargins(5,2,5,9)
           scope_layout.setSpacing(2)
           self.copy_scope = {"file": QCheckBox("File"),
                              "dir": QCheckBox("Folder"),
                              "subdir": QCheckBox("Subfolder"),
                              "name": QCheckBox("Only(Name)"),}

           for chk in self.copy_scope.values():
               chk.setChecked(True)
               scope_layout.addWidget(chk)
           self.copy_scope["name"].setChecked(False)
           scope_layout.addStretch()

           layout.addWidget(scope_group)

           # ---------------- MODE ----------------
           mode_group = QGroupBox("Copy mode")
           mode_layout = QVBoxLayout(mode_group)

           self.copy_mode = {"normal": QRadioButton("Normal copy"),
                             "multiple": QRadioButton("Multiple copies"),
                             "incremental": QRadioButton("Incremental (new / changed only)")}

           self.copy_mode["normal"].setChecked(True)


           multi_row = QHBoxLayout()
           self.copy_spin.setRange(1, 999)
           self.copy_spin.setValue(1)
           self.copy_spin.setEnabled(False)
           self.copy_spin.hide()

           spin_label = QLabel("Count")
           spin_label.hide()

           multi_row.addSpacing(20)
           multi_row.addWidget(spin_label)
           multi_row.addWidget(self.copy_spin)
           multi_row.addStretch()

           i = 0
           for rb in self.copy_mode.values():
               mode_layout.addWidget(rb)
               if i > 1:
                 break
               i+=1

           for rb in self.copy_mode.values():
               rb.toggled.connect(lambda _,spbel=spin_label: self.copier.on_clicked_copy_mode(spbel))

           mode_layout.addLayout(multi_row)
           mode_layout.addWidget(self.copy_mode["incremental"])

           layout.addWidget(mode_group)

           # ---------------- COLLISION ----------------
           collision_group = QGroupBox("If file exists")
           collision_layout = QVBoxLayout(collision_group)

           self.copy_collison = {
            "skip": QRadioButton("Skip"),
           "overwrite": QRadioButton("Overwrite"),
           "auto_rename": QRadioButton("Auto rename")}

           self.copy_collison["skip"].setChecked(True)
           for rb in self.copy_collison.values():
               collision_layout.addWidget(rb)

           layout.addWidget(collision_group)

           layout.addStretch()

           return copy_widget


        self.copy_bar.setRange(0,0)
        self.copy_bar.hide()
        bar_widget = QWidget()
        bar_layout = QHBoxLayout(bar_widget)
        bar_layout.setContentsMargins(35, 5, 5, 5)
        bar_layout.addWidget(self.copy_bar)
        bar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.copy.setText("Preview")
        copy_widget = create_copy_widget()
        copy_panel = QWidget()
        copy_panel_layout = QVBoxLayout(copy_panel)
        copy_panel_layout.setContentsMargins(0,0,0,0)
        copy_panel_layout.setSpacing(0)
        copy_panel_layout.addWidget(copy_widget)
        copy_panel_layout.addWidget(bar_widget)
        copy_panel_layout.addWidget(self.copy)
        copy_panel_layout.addStretch()


       #PREVIEW TABLE:
        self.preview_model.setHorizontalHeaderLabels(
            ["Directories", "Files"])
        self.preview_table.setModel(self.preview_model)
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        self.preview_table.verticalHeader().setVisible(False)
        self.preview_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.preview_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.preview_table.setSizePolicy(QSizePolicy.Policy.Expanding,
                                         QSizePolicy.Policy.Expanding)
        self.preview_table.setColumnWidth(0, 350)

        #BACKGROUND SCENE
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.scene.setSceneRect(0,0,self.width(),self.height())

        #ADDING VIDEO
        self.video_item.setSize(QSizeF(self.width(), self.height()))
        self.video_item.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        self.scene.addItem(self.video_item)

        #VIDEO PLAYER
        self.player.setVideoOutput(self.video_item)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.0)
        self.player.setSource(QUrl.fromLocalFile("down.mp4"))
        self.player.play()

        #STAKED WIDGETS
        self.stacked_widget.addWidget(scan_panel)
        self.stacked_widget.addWidget(rename_panel)
        self.stacked_widget.addWidget(create_panel)
        self.stacked_widget.addWidget(copy_panel)
        self.stacked_widget.setCurrentIndex(0)

       #SCREEN WIDGET:
        wrapper_layout = QVBoxLayout(self.wrapper_panels)
        wrapper_layout.setContentsMargins(0,0,0,0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(self.stacked_widget)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0,0,10,10)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.wrapper_panels)
        container_layout.addStretch()

        wrapped_widgets = QWidget()
        wrapped_layout = QHBoxLayout(wrapped_widgets)
        wrapped_layout.setContentsMargins(15,0,15,15)
        wrapped_layout.setSpacing(0)
        wrapped_layout.addWidget(self.container)
        wrapped_layout.addSpacing(15)
        wrapped_layout.addWidget(self.preview_table)

        screen_layout = QVBoxLayout(self.screen_widget)
        screen_layout.setSpacing(5)
        screen_layout.setContentsMargins(0,0,0,0)
        screen_layout.addWidget(self.mode_widget)
        screen_layout.addWidget(self.browse_widget)
        screen_layout.addWidget(wrapped_widgets)

        #stack
        self.central_widget = QWidget(self)
        stack = QStackedLayout()
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack.addWidget(self.view)
        stack.addWidget(self.screen_widget)
        self.central_widget.setLayout(stack)

        self.setCentralWidget(self.central_widget)

        #object names
        self.screen_widget.setObjectName('screen_widget')
        self.browse_widget.setObjectName("path_widget")
        self.stacked_widget.setObjectName("scan_panel")
        self.folder_path.setObjectName("path_input")
        self.mode_group.setObjectName("mode_group")
        self.browse.setObjectName("browse-btn")
        self.central_widget.setObjectName("central_widget")

        label_widget.setObjectName("label_widget")
        for label in label_widget.findChildren(QLabel):
            label.setObjectName("label")

        self.stacked_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.preview_table.setStyleSheet("background: transparent;")
        self.setStyleSheet(STYLE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    PowerManager.set_scaled_font()
    window = PowerManager()
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.show()
    sys.exit(app.exec())