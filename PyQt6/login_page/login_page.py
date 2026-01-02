import asyncio
import aiohttp
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                             QVBoxLayout, QPushButton, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget,
                             QGraphicsItem, QHBoxLayout, QStackedWidget,QStackedLayout)

from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt,QUrl,QSizeF
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
import threading
import sys


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.initUI()
        self.player.setLoops(QMediaPlayer.Loops.Infinite)

    def initUI(self):
        #window Geometry
        self.setGeometry(200,80,0,0)
        self.setFixedSize(800, 600)
        self.setWindowTitle("Login")

        #title bar
        title_bar = QWidget()
        title_bar.setFixedHeight(44)
        title_bar.setObjectName('title_bar')
        title_bar.setFixedWidth(self.width())

        title_label = QLabel("")
        title_label.setObjectName('title_label')

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(16,0,16,0)
        title_layout.setSpacing(0)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        #ICON
        window_icon = QIcon("f.jpeg")
        self.setWindowIcon(window_icon)

        #adding_Widget
        login_label = QLabel("Login Page")
        email_label = QLabel("Your Email :")
        user_email = QLineEdit()
        password_label = QLabel("Your Password :")
        user_password = QLineEdit()
        submit_button = QPushButton("Submit")

        #adding PlaceHoler yada yada
        user_email.setPlaceholderText("Enter email here...")
        user_password.setPlaceholderText("Enter password here...")
        user_password.setEchoMode(QLineEdit.EchoMode.Password)


        #login_label
        user_email.setFixedHeight(40)
        user_password.setFixedHeight(40)
        submit_button.setFixedHeight(44)
        submit_button.setFixedWidth(300)
        login_label.setFixedWidth(110)
        login_label.setFixedHeight(40)
        login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #form form_layout
        card = QWidget()
        card.setFixedSize(350, 340)
        form_widget = QWidget(card)
        form_layout = QVBoxLayout()
        form_widget.setLayout(form_layout)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(form_widget)

        #adding widget to the form_layout
        form_layout.addWidget(login_label,alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addSpacing(30)
        form_layout.addWidget(email_label)
        form_layout.addWidget(user_email)
        form_layout.addSpacing(10)
        form_layout.addWidget(password_label)
        form_layout.addWidget(user_password)
        form_layout.addSpacing(30)
        form_layout.addWidget(submit_button,alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.setContentsMargins(20,20,20,20)


        #QGraphics
        scene = QGraphicsScene()
        view = QGraphicsView()
        view.setScene(scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        view.setFrameShape(QGraphicsView.Shape.NoFrame)
        scene.setSceneRect(0, 0, self.width(), self.height())

        video_item = QGraphicsVideoItem()
        video_item.setSize(QSizeF(self.width(),self.height()))
        video_item.setAspectRatioMode(Qt.AspectRatioMode.IgnoreAspectRatio)
        scene.addItem(video_item)

        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(video_item)
        self.audio.setVolume(0.0)
        self.player.setSource(QUrl.fromLocalFile("up.mp4"))
        self.player.play()


        proxy = QGraphicsProxyWidget()
        proxy.setWidget(card)
        proxy.setPos((self.width() - form_widget.width())//2,
                  (self.height() - form_widget.height())//2)
        proxy.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsChildrenToShape)
        proxy.setZValue(1)
        scene.addItem(proxy)

        # central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        stack = QStackedLayout()
        stack.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stack.addWidget(view)
        stack.addWidget(title_bar)
        central_widget.setLayout(stack)

        #Adding Object Names
        login_label.setObjectName("login_page")
        email_label.setObjectName("email_label")
        user_email.setObjectName("user_email")
        password_label.setObjectName("password_label")
        user_password.setObjectName("user_password")
        submit_button.setObjectName("submit_button")
        form_widget.setObjectName("form_widget")
        form_layout.setObjectName("form_layout")
        card.setObjectName("card")

        #StyleSheet
        form_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        form_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        form_widget.setAutoFillBackground(False)
        card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        card.setAutoFillBackground(True)


        self.setStyleSheet("""QMainWindow{
    background-color: transparent;
    border-radius: 18px;
    border: 1.5px solid rgba(255, 255, 255, 90);
            
        }""")


        card.setStyleSheet("""
QWidget#card {
    background-color: transparent;
    border-radius: 18px;
    border: 1.5px solid rgba(255, 255, 255, 90);
}

        """)
        form_widget.setStyleSheet("""
        
        QLabel#login_page{
            border: 1px solid rgba(255, 255, 255, 90);
            color: rgba(230, 230, 230, 210);
            font-size: 20px;
            border-radius: 10px;
        }
        
        QLabel{
        
        background: transparent;
        
        }
        
        QLabel#email_label{
            background: transparent;
            color: rgba(230, 230, 230, 210);
            font-size: 10px;
            
        } 
        
        QLabel#password_label{
            background: transparent;
            color: rgba(230, 230, 230, 210);
            font-size: 10px;
        }
        

        QLineEdit {
    background-color: rgba(0, 0, 0, 190);
    color: white;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,35);
    padding: 9px 12px;
}


        QLineEdit:focus {
            border: 1px solid rgba(255, 255, 255, 90);
            background-color: rgba(0, 0, 0, 180);
        }

QPushButton {
    background-color: rgb(85, 85, 100);
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
    border: 1px solid rgba(255,255,255,40);
}

/* hover */
QPushButton:hover {
    background-color: rgb(100, 100, 120);
    border: 1px solid rgba(255,255,255,80);
}

/* pressed (mouse down) */
QPushButton:pressed {
    background-color: rgb(70, 70, 85);
    border: 1px solid rgba(255,255,255,60);
}


        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec())