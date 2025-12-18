from PyQt6.QtGui import QIcon, QPainter,QStandardItemModel,QStandardItem,QAction

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
, QLabel, QLineEdit, QStackedLayout, QGraphicsView,
                             QGraphicsScene, QFileDialog,
                             QStackedWidget, QButtonGroup, QTableView, QToolButton, QSizePolicy, QCheckBox,QGroupBox)

from PyQt6.QtCore import Qt, QSizeF, QUrl
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem

import sys


from WorkerManager import ScanManager


class PowerManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scope_wrapped = None
        self.scope_box = None
        self.browse_widget = None
        self.vertical_widget = None
        self.mode_layout = None
        self.mode_widget = None
        self.container = None
        self.wrapped_panel = None
        self.wrapper_panels = None

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

        #preview table
        self.preview_table = QTableView()
        self.preview_model = QStandardItemModel(0, 2)

        #row buttons
        self.btn_scan = QToolButton()
        self.btn_rename = QToolButton()
        self.btn_move = QToolButton()
        self.btn_dirs = QToolButton()
        self.btn_files = QToolButton()
        self.mode_group = QButtonGroup()

        #stackWidget
        self.stacked_widget = QStackedWidget()

        #Graphics Item
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.video_item = QGraphicsVideoItem()

        #labels
        self.dirs_label = QLabel("Folder :")
        self.files_label = QLabel("Files :")
        self.subdirs_label = QLabel("Subdirs :")
        self.extension_label = QLabel("Specific Extension: ?")

        #lineedits
        self.folder_path = QLineEdit()
        self.extension = QLineEdit()

        #checkboxes
        self.chk_files = QCheckBox("Files")
        self.chk_dirs = QCheckBox("Folders")
        self.chk_subdirs = QCheckBox("SubFolders")
        self.chk_hidden = QCheckBox("Include Hidden")

        #buttons
        self.browse = QPushButton("📂")
        self.scan = QPushButton("SCAN")
        self.apply_rename_btn = QPushButton("Apply")

        #screen widget
        self.screen_widget = QWidget()
        self.screen_layout = QVBoxLayout(self.screen_widget)

        #central widget
        self.central_widget = QWidget(self)


        #WorkerClasses
        self.scanner = ScanManager(self)


        #UI
        self.InitUi()

        #connections
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.browse.clicked.connect(self.browse_dirs)
        self.scan.clicked.connect(lambda: self.scanner.scan(self.folder_path.text()))

        #radio buttons
        self.mode_group.idClicked.connect(self.stacked_widget.setCurrentIndex)



    def update_scanned_counts(self,dirs,files,subdirs):
        self.dirs_label.setText(f"Folders : {dirs}")
        self.files_label.setText(f"Files : {files}")
        self.subdirs_label.setText(f"Subdirs : {subdirs}")


    def browse_dirs(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder"
                                                  ,"",QFileDialog.Option.ShowDirsOnly)
        if folder:
            self.folder_path.setText(folder)
            self.folder_path.setReadOnly(False)


    def resizeEvent(self,event):
         super().resizeEvent(event)

         new_width = self.central_widget.width()
         new_height = self.central_widget.height()

         #VIDEO ITEM
         self.scene.setSceneRect(0,0,new_width,new_height)
         self.video_item.setSize(QSizeF(new_width,new_height))


         #MODE AREA
         self.mode_widget.setMaximumSize(int(new_width),int(new_height*0.090 ))


         #BROWSE AREA
         self.browse_widget.setMaximumSize(int(new_width*0.4),int(new_height*0.088))
         browse_width,browse_height = self.browse_widget.width(), self.browse_widget.height()
         self.browse.setMaximumSize(int(browse_width*0.15),int(browse_height*0.7))
         self.folder_path.setMaximumHeight(int(browse_height*0.7))


         #PANELS
         self.wrapper_panels.setMaximumWidth(int(new_width * 0.25))
         self.wrapper_panels.setMaximumHeight(int(new_height * 0.35))
         panel_width = self.wrapper_panels.width()
         panel_height = self.wrapper_panels.height()
         print(panel_width,panel_height)

         #SCAN PANEL




         self.container.setMaximumSize(int(new_width * 0.25)
                                      ,new_height)

         self.preview_table.setMaximumWidth(int(new_width * 0.74))
         self.preview_table.setMaximumHeight(int(new_height * 0.75))


    def InitUi(self):

       #WINDOW:
        self.setWindowTitle("Made By DvLKing20")
        self.setWindowIcon(QIcon("f.jpeg"))
        self.resize(1000,600)

       #TOP BUTTONS:
        self.btn_scan.setText("Scan")
        self.btn_rename.setText("Rename")
        self.btn_move.setText("Move")
        self.btn_dirs.setText("Create Folders")
        self.btn_files.setText("Create Files")
        self.mode_group.setExclusive(True)

        self.mode_group.addButton(self.btn_scan, 0)
        self.mode_group.addButton(self.btn_rename, 1)
        self.mode_group.addButton(self.btn_move, 2)
        self.mode_group.addButton(self.btn_dirs, 3)
        self.mode_group.addButton(self.btn_files, 4)
        self.btn_scan.setChecked(True)

        self.mode_widget = QWidget()
        mode_layout = QHBoxLayout(self.mode_widget)
        mode_layout.setSpacing(0)
        mode_layout.addWidget(self.btn_scan)
        mode_layout.addWidget(self.btn_rename)
        mode_layout.addWidget(self.btn_move)
        mode_layout.addWidget(self.btn_dirs)
        mode_layout.addWidget(self.btn_files)
        mode_layout.addStretch()
        self.mode_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.btn_scan.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_rename.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_move.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_dirs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.btn_files.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        for btn in (
            self.btn_scan,
            self.btn_rename,
            self.btn_move,
            self.btn_dirs,
            self.btn_files,
        ):
           btn.setCheckable(True)
           btn.setFixedHeight(30)
           btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
           btn.setCursor(Qt.CursorShape.PointingHandCursor)


       #BROWSE PANEL:
        self.folder_path.setPlaceholderText("Choose a folder...")
        self.browse.setCursor(Qt.CursorShape.PointingHandCursor)

        self.browse_widget = QWidget()
        browse_layout = QHBoxLayout(self.browse_widget)
        browse_layout.addWidget(self.folder_path)
        browse_layout.addWidget(self.browse)
        self.browse_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.browse.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.folder_path.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)


       #SCAN PANEL:
        self.scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.extension.setPlaceholderText("Ignore if not...")
        self.chk_files.setChecked(True)
        self.chk_dirs.setChecked(True)

        scan_widget = QWidget()
        scan_layout = QHBoxLayout(scan_widget)
        scan_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scan_layout.setContentsMargins(6,0,0,0)
        scan_layout.addWidget(self.extension,alignment=Qt.AlignmentFlag.AlignLeft)
        scan_layout.addWidget(self.scan,alignment=Qt.AlignmentFlag.AlignRight)

        label_widget = QWidget()
        label_layout = QVBoxLayout(label_widget)
        label_layout.setSpacing(5)
        label_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        label_layout.addWidget(self.dirs_label)
        label_layout.addWidget(self.files_label)
        label_layout.addWidget(self.subdirs_label)

        self.scope_box = QGroupBox("Scan scope")
        layout = QVBoxLayout(self.scope_box)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.chk_files)
        layout.addWidget(self.chk_dirs)
        layout.addWidget(self.chk_subdirs)
        layout.addWidget(self.chk_hidden)
        self.scope_box.setSizePolicy(
        QSizePolicy.Policy.Preferred,
        QSizePolicy.Policy.Preferred
                                    )

        self.scope_wrapped = QWidget()
        scope_box_label_layout = QHBoxLayout(self.scope_wrapped)
        scope_box_label_layout.setSpacing(0)
        scope_box_label_layout.setContentsMargins(10,5,0,0)
        scope_box_label_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scope_box_label_layout.addWidget(self.scope_box)
        scope_box_label_layout.addWidget(label_widget,alignment=Qt.AlignmentFlag.AlignRight)
        self.scope_wrapped.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred )

        scan_panel = QWidget()
        scan_panel_layout = QVBoxLayout(scan_panel)
        scan_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scan_panel_layout.addWidget(self.extension_label,alignment=Qt.AlignmentFlag.AlignLeft)
        scan_panel_layout.addWidget(scan_widget,alignment=Qt.AlignmentFlag.AlignLeft)
        scan_panel_layout.addWidget(self.scope_wrapped)

       #RENAME PANEL:
        self.apply_rename_btn.setFixedSize(150,40)
        rename_panel = QWidget()
        rename_panel_layout = QVBoxLayout(rename_panel)
        rename_panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        rename_panel_layout.addWidget(self.apply_rename_btn)




       #PREVIEW TABLE:
        self.preview_model.setHorizontalHeaderLabels(
            ["Original Name", "Preview"])
        self.preview_table.setModel(self.preview_model)
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        self.preview_table.verticalHeader().setVisible(False)
        self.preview_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.preview_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.preview_table.setSizePolicy(QSizePolicy.Policy.Expanding,
                                         QSizePolicy.Policy.Expanding)




        #background_scene
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.scene.setSceneRect(0,0,self.width(),self.height())

        #adding video
        self.video_item.setSize(QSizeF(self.width(), self.height()))
        self.video_item.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        self.scene.addItem(self.video_item)

        #player
        self.player.setVideoOutput(self.video_item)
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.0)
        self.player.setSource(QUrl.fromLocalFile("down.mp4"))
        self.player.play()


        #stacked_widget
        self.stacked_widget.addWidget(scan_panel)
        self.stacked_widget.addWidget(rename_panel)
        self.stacked_widget.setCurrentIndex(0)

       #SCREEN WIDGET:

        self.wrapper_panels = QWidget()
        wrapper_layout = QVBoxLayout(self.wrapper_panels)
        wrapper_layout.setContentsMargins(0,0,0,0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(self.stacked_widget)
        self.wrapper_panels.setSizePolicy(
        QSizePolicy.Policy.Preferred,
        QSizePolicy.Policy.Preferred
                          )


        self.container = QWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0,0,0,0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.wrapper_panels)
        container_layout.addStretch()


        wrapped_widgets = QWidget()
        wrapped_layout = QHBoxLayout(wrapped_widgets)
        wrapped_layout.setContentsMargins(0,0,0,0)
        wrapped_layout.setSpacing(0)
        wrapped_layout.addWidget(self.container)
        wrapped_layout.addWidget(self.preview_table)


        self.screen_layout.setContentsMargins(0,0,0,0)
        self.screen_layout.setSpacing(20)
        self.screen_layout.addWidget(self.mode_widget)
        self.screen_layout.addWidget(self.browse_widget)
        self.screen_layout.addWidget(wrapped_widgets)


        #stack
        stack = QStackedLayout()
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack.addWidget(self.view)
        stack.addWidget(self.screen_widget)
        self.central_widget.setLayout(stack)

        self.setCentralWidget(self.central_widget)


        #object names
        self.screen_widget.setObjectName('screen_widget')
        label_widget.setObjectName("label_widget")
        self.browse_widget.setObjectName("path_widget")
        scan_panel.setObjectName("scan_panel")
        self.folder_path.setObjectName("folder_path")
        self.mode_group.setObjectName("mode_group")


        self.stacked_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.preview_table.setStyleSheet("background: transparent;")

        self.setStyleSheet("""
        
        
QWidget#screen_widget {

    background-color: rgba(30, 32, 36, 180);
    border: 1.5px solid #35414d;
    border-radius: 10px;
    padding: 10px;
}


QWidget#scan_panel {

    background-color: rgba(22, 24, 28, 200);
    border: 3px solid #424c4f;
    border-radius: 14px;
    padding: 10px;
}

/* <--------Buttons----------> */
        
QPushButton{
    background-color: rgba(40, 44, 52, 200);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,80);
    border-radius: 10px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: rgba(60, 65, 75, 220);
}

QPushButton:pressed {
    background-color: rgba(80, 120, 200, 220);
}

/* <---------------- BUTTONS MODES -------------->*/

QToolButton {
    background-color: rgba(32, 35, 42, 140);
    color: #d6d9e0;
    border: 1px solid rgba(255,255,255,35);
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
    min-width: 110px;
}


/* rounded ends only */
QToolButton:first-child {
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
}

QToolButton:last-child {
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

/* subtle hover – not loud, not ugly */
QToolButton:hover {
    background-color: rgba(55, 60, 70, 180);
    box-shadow: inset 0 1px 0 rgba(255,255,255,60);
}


/* active mode – clean highlight */
QToolButton:checked {
    background-color: rgba(120, 170, 255, 220);
    color: #ffffff;
    border-color: rgba(180,210,255,255);
    font-weight: 600;
}

/* pressed feedback */
QToolButton:pressed {
    background-color: rgba(90, 130, 200, 220);
}

/* <---------------- PATH INPUT -------------->*/

QLineEdit#folder_path {
    background-color: #1c1d20;
    border: 1px solid #3a3d44;
    font-size: 12px;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e6e6e6;
}

QLineEdit#folder_path:focus {
    border: 1.5px solid #6f85ff;
    background-color: #202126;
}
/* <---------------- LABELS -------------->*/

QLabel {
    color: #cfd2da;
    font-size: 15px;
    padding: 1px 6px;
}

QLabel:hover {
    color: #ffffff;
    background-color: #2a2c31;
    border-radius: 4px;
    border: 1px solid #cfd2da;
}

/* <---------------------- TABLE VIEW --------------> */


QTableView {
    background-color: rgba(20, 22, 26, 140);
    color: #e6e8ec;
    border: 1.5px solid rgba(255, 255, 255, 40);
    border-radius: 10px;
    gridline-color: rgba(255, 255, 255, 25);
    selection-background-color: rgba(120, 170, 255, 120);
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: rgba(30, 32, 36, 180);
    color: #dfe3ea;
    padding: 6px;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 60);
    font-weight: 600;
}

QTableView::item {
    padding: 6px;
    background-color: transparent;
}

QTableView::item:hover {
    background-color: rgba(255, 255, 255, 30);
}

QTableView::item:selected:hover {
    background-color: rgba(120, 170, 255, 160);
}

/* ================== GLOBAL LINEEDIT ================== */

QLineEdit {
    background-color: rgba(28, 30, 34, 200);
    color: #e6e8ec;

    border: 1.5px solid rgba(255, 255, 255, 45);
    border-radius: 8px;

    padding: 6px 10px;
    font-size: 13px;

    selection-background-color: rgba(120, 170, 255, 180);
    selection-color: #ffffff;
}

/* Hover – subtle, not annoying */
QLineEdit:hover {
    border-color: rgba(160, 190, 255, 120);
}

/* Focus – clear but not neon */
QLineEdit:focus {
    background-color: rgba(32, 34, 40, 230);
    border: 2px solid rgba(120, 170, 255, 220);
}

/* Placeholder text */
QLineEdit::placeholder {
    color: rgba(200, 200, 200, 120);
    font-style: italic;
}

/* Read-only */
QLineEdit:read-only {
    background-color: rgba(22, 24, 28, 180);
    color: rgba(200, 200, 200, 160);
    border-style: dashed;
}

/* Disabled */
QLineEdit:disabled {
    background-color: rgba(18, 20, 24, 160);
    color: rgba(180, 180, 180, 120);
    border-color: rgba(255, 255, 255, 25);
}




""")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PowerManager()
    window.show()
    sys.exit(app.exec())