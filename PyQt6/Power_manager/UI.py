from PyQt6.QtGui import QIcon, QPainter,QStandardItemModel

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
, QLabel, QLineEdit, QStackedLayout, QGraphicsView,
                             QGraphicsScene, QStackedWidget,
                             QButtonGroup, QTableView, QToolButton, QSizePolicy, QCheckBox,QGroupBox)

from PyQt6.QtCore import Qt, QSizeF, QUrl
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem

import sys
import WorkerManager


class PowerManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

        #PREVIEW TABLE
        self.preview_table = QTableView()
        self.preview_model = QStandardItemModel(0, 1)

        #TOOL BUTTONS
        self.btn_scan = QToolButton()
        self.btn_rename = QToolButton()
        self.btn_move = QToolButton()
        self.btn_dirs = QToolButton()
        self.btn_files = QToolButton()
        self.btn_name = QToolButton()
        self.mode_group = QButtonGroup()

        #WIDGETS
        self.central_widget = None
        self.screen_widget = None
        self.label_widget = None
        self.stacked_widget = None
        self.browse_widget = None
        self.mode_widget = None
        self.container = None
        self.wrapper_panels = None
        self.scope_wrapped = None

        #Graphics Item
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.video_item = QGraphicsVideoItem()

        #LABELS
        self.dirs_label = QLabel("Folders : 0")
        self.files_label = QLabel("Files : 0")
        self.subdirs_label = QLabel("Subdirs : 0")
        self.extension_label = QLabel("Specific Extension: ?")

        #LINE EDITS
        self.folder_path = QLineEdit()
        self.extension = QLineEdit()

        #CHECKBOXES
        self.scope_box = None
        self.chk_files = QCheckBox("Files")
        self.chk_dirs = QCheckBox("Folders")
        self.chk_subdirs = QCheckBox("SubFolders")
        self.chk_preview = QCheckBox("Preview Only")
        self.chk_hidden = QCheckBox("Include Hidden")

        #BUTTONS
        self.browse = QPushButton("📂")
        self.scan = QPushButton("SCAN")
        self.apply_rename_btn = QPushButton("Apply")

        #WorkerClasses
        self.scanner = WorkerManager.ScanManager(self)

        #UI
        self.InitUi()


        #TOOL BUTTON CONNECTIONS
        self.mode_group.idClicked.connect(self.stacked_widget.setCurrentIndex)

        #CONNECTIONS
        self.player.setLoops(QMediaPlayer.Loops.Infinite)
        self.browse.clicked.connect(lambda: WorkerManager.browse_dirs(self))
        self.scan.clicked.connect(lambda: self.scanner.scan(self.folder_path.text()))



    def resizeEvent(self,event):
         super().resizeEvent(event)

         new_width = self.central_widget.width()
         new_height = self.central_widget.height()

         #VIDEO ITEM
         self.scene.setSceneRect(0,0,new_width,new_height)
         self.video_item.setSize(QSizeF(new_width,new_height))


         #mode buttons
         self.mode_widget.setMaximumSize(new_width,int(new_height*0.090))



         #BROWSE AREA
         self.browse_widget.setMaximumSize(int(new_width*0.35),int(new_height*0.093))



         self.container.setMaximumSize(int(new_width * 0.28)
                                      ,new_height)




    def InitUi(self):

       #WINDOW:
        self.setWindowTitle("Made By DvLKing20")
        self.setWindowIcon(QIcon("f.jpeg"))
        self.resize(1000,650)


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
        self.mode_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        for btn in (
            self.btn_scan,
            self.btn_rename,
            self.btn_move,
            self.btn_dirs,
            self.btn_files,
        ):
           btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
           btn.setCheckable(True)
           btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
           btn.setCursor(Qt.CursorShape.PointingHandCursor)


       #BROWSE PANEL:
        self.folder_path.setPlaceholderText("Choose a folder...")
        self.browse.setCursor(Qt.CursorShape.PointingHandCursor)

        self.browse_widget = QWidget()
        browse_layout = QHBoxLayout(self.browse_widget)
        browse_layout.setSpacing(5)
        browse_layout.setContentsMargins(10, 8, 10, 10)
        browse_layout.addWidget(self.folder_path)
        browse_layout.addWidget(self.browse)
        self.folder_path.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.browse.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.browse_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


       #SCAN PANEL:
        self.scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.extension.setPlaceholderText("Choose a folder first...")
        self.chk_files.setChecked(True)
        self.chk_dirs.setChecked(True)
        self.scan.setDisabled(True)

        scan_widget = QWidget()
        scan_layout = QHBoxLayout(scan_widget)
        scan_layout.setContentsMargins(10,10,10,10)
        scan_layout.setSpacing(4)
        scan_layout.addWidget(self.extension)
        scan_layout.addWidget(self.scan)

        self.label_widget = QWidget()
        label_layout = QVBoxLayout(self.label_widget)
        label_layout.setSpacing(10)
        label_layout.addWidget(self.dirs_label)
        label_layout.addWidget(self.files_label)
        label_layout.addWidget(self.subdirs_label)
        self.label_widget.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.dirs_label.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.files_label.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        self.subdirs_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.scope_box = QGroupBox("Scan scope")
        layout = QVBoxLayout(self.scope_box)
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(3)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.chk_files)
        layout.addWidget(self.chk_dirs)
        layout.addWidget(self.chk_subdirs)
        layout.addWidget(self.chk_preview)
        layout.addWidget(self.chk_hidden)
        self.scope_box.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Expanding)

        self.scope_wrapped = QWidget()
        scope_box_label_layout = QHBoxLayout(self.scope_wrapped)
        scope_box_label_layout.setSpacing(5)
        scope_box_label_layout.setContentsMargins(10,10,10,15)
        scope_box_label_layout.addWidget(self.scope_box)
        scope_box_label_layout.addWidget(self.label_widget)
        self.scope_wrapped.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding )

        scan_panel = QWidget()
        scan_panel_layout = QVBoxLayout(scan_panel)
        scan_panel_layout.setContentsMargins(10,10,10,10)
        scan_panel_layout.setSpacing(0)
        scan_panel_layout.addWidget(self.extension_label)
        scan_panel_layout.addWidget(scan_widget)
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
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(scan_panel)
        self.stacked_widget.addWidget(rename_panel)
        self.stacked_widget.setCurrentIndex(0)

       #SCREEN WIDGET:

        self.wrapper_panels = QWidget()
        wrapper_layout = QVBoxLayout(self.wrapper_panels)
        wrapper_layout.setContentsMargins(0,0,0,0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(self.stacked_widget)


        self.container = QWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0,0,0,0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.wrapper_panels)
        container_layout.addStretch()


        wrapped_widgets = QWidget()
        wrapped_layout = QHBoxLayout(wrapped_widgets)
        wrapped_layout.setContentsMargins(10,10,10,10)
        wrapped_layout.setSpacing(5)
        wrapped_layout.addWidget(self.container)
        wrapped_layout.addSpacing(20)
        wrapped_layout.addWidget(self.preview_table)

        self.screen_widget = QWidget()
        screen_layout = QVBoxLayout(self.screen_widget)
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
        self.label_widget.setObjectName("label_widget")
        self.browse_widget.setObjectName("path_widget")
        scan_panel.setObjectName("scan_panel")
        self.folder_path.setObjectName("path_input")
        self.mode_group.setObjectName("mode_group")
        self.browse.setObjectName("browse-btn")
        for label in self.label_widget.findChildren(QLabel):
          label.setObjectName("label")

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
        
QPushButton {
    
    background-color: rgba(40, 44, 52, 210);
    color: #e6e8ec;

    border: 1.5px solid rgba(255, 255, 255, 70);
    border-radius: 10px;
    font-family: Comic Sans MS;
    padding: 8px 16px;
    font-size: 12px;
    font-weight: 600;
}

/* hover – brighter surface, sharper edge */
QPushButton:hover {
    background-color: rgba(55, 60, 70, 235);
    border-color: rgba(255, 255, 255, 140);
}

/* pressed – darker, solid, confident */
QPushButton:pressed {
    background-color: rgba(30, 32, 36, 245);
    border-color: rgba(255, 255, 255, 200);
}

/* keyboard focus – white glow (not cyan) */
QPushButton:focus {
    outline: none;
    border: 2px solid rgba(255, 255, 255, 220);
    box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 70),
        0 0 6px rgba(255, 255, 255, 90);
}

/* checked / active state (soft grey highlight) */
QPushButton:checked {
    background-color: rgba(70, 75, 85, 240);
    color: #ffffff;
    border-color: rgba(200, 200, 200, 200);
}

/* disabled – obvious but not ugly */
QPushButton:disabled {
    background-color: rgba(38, 40, 44, 120);
    color: rgba(200, 200, 200, 90);
    border-color: rgba(255, 255, 255, 30);
}

/* disabled safety */
QPushButton:disabled:hover,
QPushButton:disabled:pressed {
    background-color: rgba(38, 40, 44, 120);
}


QPushButton#browse_btn {
    background-color: rgba(38, 42, 48, 220);
    color: #e6e8ec;

    border: 1.5px solid rgba(255, 255, 255, 60);
    border-radius: 8px;

    padding: 6px 14px;
    font-size: 14px;
    font-weight: 600;
}

/* hover → slightly brighter surface + clearer edge */
QPushButton#browse_btn:hover {
    background-color: rgba(50, 55, 62, 235);
    border-color: rgba(255, 255, 255, 120);
}

/* pressed → darker surface, crisp edge */
QPushButton#browse_btn:pressed {
    background-color: rgba(28, 30, 34, 240);
    border-color: rgba(255, 255, 255, 180);
}

/* disabled → flat, obvious, not ugly */
QPushButton#browse_btn:disabled {
    background-color: rgba(32, 34, 38, 120);
    color: rgba(200, 200, 200, 80);
    border-color: rgba(255, 255, 255, 25);
}

/* disabled hover safety */
QPushButton#browse_btn:disabled:hover,
QPushButton#browse_btn:disabled:pressed {
    background-color: rgba(32, 34, 38, 120);
}

/* <---------------- BUTTONS MODES -------------->*/

QToolButton {
    font-family: Comic Sans MS;
    background-color: rgba(30, 33, 40, 180);
    color: #dfe6ff;

    border: 1.5px solid rgba(255,255,255,45);
    border-bottom: 3px solid rgba(255,255,255,25);

    padding: 10px 22px;
    font-size: 14px;
    font-weight: 600;

    min-width: 120px;

    transition: all 150ms ease;
}

QToolButton:hover {
    background-color: rgba(120, 35, 40, 220);
    border-color: rgba(255, 120, 120, 220);

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,80),
        0 0 14px rgba(255, 80, 80, 180);
}

QToolButton:pressed {
    background-color: rgba(170, 40, 45, 240);
    border-bottom: 2px solid rgba(120, 20, 25, 255);

    box-shadow:
        inset 0 4px 8px rgba(0,0,0,200),
        0 0 10px rgba(255, 60, 60, 200);
}

/* CHECKED – red = active mode */
QToolButton:checked {
    background-color: rgba(180, 55, 55, 235);
    color: #ffffff;

    border-color: rgba(255, 200, 200, 220);
    font-weight: 600;
}

QToolButton:disabled {
    background-color: rgba(28, 30, 36, 120);
    color: rgba(200,200,200,90);
    border: 1px solid rgba(255,255,255,25);
}

QToolButton:first-child {
    border-top-left-radius: 14px;
    border-bottom-left-radius: 14px;
}

QToolButton:last-child {
    border-top-right-radius: 14px;
    border-bottom-right-radius: 14px;
}


/* <---------------- PATH INPUT -------------->*/

QLineEdit#path_input {

    font-family: Comic Sans MS;
    background-color: rgba(24, 26, 30, 230);
    color: #e6e8ec;

    border: 1.5px solid rgba(255, 255, 255, 55);
    border-radius: 8px;

    padding: 6px 10px;
    font-size: 13px;
}

/* hover → clean edge, no glow yet */
QLineEdit#path_input:hover {
    border-color: rgba(255, 255, 255, 110);
}

/* focus → white glow (soft, professional) */
QLineEdit#path_input:focus {
    background-color: rgba(28, 30, 34, 240);

    border: 2px solid rgba(255, 255, 255, 200);

    /* fake glow via inset + outer highlight */
    box-shadow:
        inset 0 0 0 1px rgba(255, 255, 255, 60),
        0 0 6px rgba(255, 255, 255, 80);
}

/* placeholder text */
QLineEdit#path_input::placeholder {
    color: rgba(200, 200, 200, 120);
    font-style: italic;
}

/* read-only → intentional, not dead */
QLineEdit#path_input:read-only {
    background-color: rgba(22, 24, 28, 200);
    color: rgba(200, 200, 200, 160);
    border-style: dashed;
}

/* disabled → visually clear */
QLineEdit#path_input:disabled {
    background-color: rgba(20, 22, 26, 160);
    color: rgba(180, 180, 180, 120);
    border-color: rgba(255, 255, 255, 25);
}


/* <---------------- LABELS -------------->*/

QLabel {
    font-family: Comic Sans MS;
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

QLabel#label{
    color: #ffffff;
    background-color: #2a2c31;
    border-radius: 4px;
    border: 0.8px solid #cfd2da;
}

/* <---------------------- TABLE VIEW --------------> */


QTableView {

    font-family: Comic Sans MS;
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
    font-family: Comic Sans MS;
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