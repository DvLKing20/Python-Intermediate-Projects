import asyncio
import aiohttp
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QProgressBar,
                             QPushButton,QWidget,QLabel,QVBoxLayout,QLineEdit,QScrollArea,QHBoxLayout,)
from PyQt5.QtCore import Qt,pyqtSignal
import threading
import sys


class DownloadManager(QMainWindow):
    #class variable for setting up download signals
    set_range = pyqtSignal(int, int)
    set_value = pyqtSignal(int,int)
    set_text = pyqtSignal(int,str)


    def __init__(self):
        super().__init__()
        #storing sessions
        self.sessions = []
        self.urls = []
        self.path = ""
        self.progress_bars = []
        # Widgets
        self.label_url = QLabel("                 Paste a URL to start downloading")
        self.add_url = QLineEdit()
        self.add_url_button = QPushButton("Add Download")
        self.start_DL = QPushButton("Start Downloads")
        #scrollArea widget
        self.scrollArea = QScrollArea()
        self.job_container = QWidget()
        self.job_container_layout = QVBoxLayout()
        #userpath widget
        self.user_path = QLineEdit()
        self.user_path_button = QPushButton("Add Path")
        #mainwindow widget
        self.widget = QWidget()
        self.QVBoxLayout = QVBoxLayout()
        # Setup UI
        self.initUI()
        self.user_path_button.clicked.connect(self.fetch_user_path)
        self.add_url_button.clicked.connect(self.extract_url)
        self.start_DL.clicked.connect(self.start_download)
        #connecting the signals
        self.set_range.connect(self.on_set_range)
        self.set_value.connect(self.on_set_value)
        self.set_text.connect(self.on_set_text)

    def on_set_range(self,content_length: int, index: int):
      if 0 <= index < len(self.progress_bars):
        bar = self.progress_bars[index]
        bar.setRange(0, content_length)
        bar.setValue(0)

    def on_set_value(self,downloaded: int,index: int):
       if 0 <= index < len(self.progress_bars):
        bar = self.progress_bars[index]
        bar.setValue(downloaded)

    def on_set_text(self,index: int,format: str):
        if 0 <= index < len(self.progress_bars):
            bar = self.progress_bars[index]
            bar.setTextVisible(True)
            bar.setFormat(format)

    def fetch_user_path(self):
         self.path = self.user_path.text()


    async def fetch_url(self,user_url: str,session: aiohttp.ClientSession,index: int):
        try:
           path = Path(self.path)
           path.mkdir(parents=True, exist_ok=True)
           file_name = user_url.split("/")[-1]
           full_path = path/file_name
           async with session.get(user_url) as resp:
                content_length = resp.headers.get("Content-Length")
                #don't blast my code why! sometimes headers content length gives None
                try:
                   content_length = int(content_length) if content_length is not None else 0
                except (TypeError,ValueError):
                     content_length = 0

                self.set_range.emit(content_length, index)

                downloaded = 0

                #writing in the file as binary
                with open(full_path,"wb") as f:
                  async for chunk in resp.content.iter_chunked(4096):
                      f.write(chunk)
                      downloaded += len(chunk)
                      self.set_value.emit(downloaded, index)

                      #formatting the stuff
                      if content_length > 0:
                          mb_done = downloaded / (1024 * 1024)
                          mb_total = content_length / (1024 * 1024)
                          format = f"{file_name}: {mb_done:.2f} / {mb_total:.2f} MB"
                          self.set_text.emit(index,format)
                      #await bruh
                      await asyncio.sleep(0)

        except aiohttp.ClientError as e:
             print("Client Error Occured: ",e)
        except aiohttp.ClientConnectorError as e:
             print("Error No Internet Connection: ",e)
        except aiohttp.ClientTimeout as e:
             print("Timeout Error: ",e)
        except Exception as e:
             print("Exception Occured: ",e)


    def start_download(self):
        async def main():
            async with aiohttp.ClientSession() as session:
             for index,url in enumerate(self.urls):
                 task = asyncio.create_task(self.fetch_url(url,session,index))
                 self.sessions.append(task)
             await asyncio.gather(*self.sessions)
             del self.sessions[:]
             del self.urls[:]
             del self.progress_bars[:]
             #clean up the progress bar after completed
             # layout = self.job_container_layout
             # while layout.count():
             #    take_item = layout.takeAt(0)
             #    take_widget = take_item.widget()
             #    if take_widget is not None:
             #        take_widget.deleteLater()

        #checking if url start with http or https
        thread = threading.Thread(target=lambda:asyncio.run(main()))
        thread.start()


    def extract_url(self):
      extracted_url = self.add_url.text()
      user_url = extracted_url.strip()
      if user_url.startswith(("https://", "http://")):
        self.urls.append(user_url)
        self.add_url.setText("")
        bar = QProgressBar()
        self.progress_bars.append(bar)
        self.job_container_layout.addWidget(bar,alignment=Qt.AlignTop)


    def initUI(self):
        self.user_path.setPlaceholderText("Enter path here...")
        self.add_url.setPlaceholderText("Enter it here...")

        #Name of the Download title and stuff
        self.setWindowTitle("King_DL_Manager")
        self.setGeometry(400, 200, 1000, 800)
        self.setFixedSize(1000, 800)

        #top part labels
        self.QVBoxLayout.addWidget(self.label_url, alignment=Qt.AlignTop)
        self.QVBoxLayout.addWidget(self.add_url, alignment=Qt.AlignCenter)

        #add urls and start downloading buttons
        button_row = QHBoxLayout()
        button_row.addWidget(self.add_url_button)
        button_row.addWidget(self.start_DL)
        button_row.setSpacing(20)
        button_row.setAlignment(Qt.AlignCenter)
        self.QVBoxLayout.addLayout(button_row)

        #scroll area
        self.QVBoxLayout.addWidget(self.scrollArea, alignment=Qt.AlignCenter| Qt.AlignBottom)

        # --- Path input row ---
        path_row = QHBoxLayout()
        path_row.addWidget(self.user_path_button)
        path_row.addWidget(self.user_path,alignment=Qt.AlignBottom)

        self.QVBoxLayout.addLayout(path_row)

        self.widget.setLayout(self.QVBoxLayout)
        self.setCentralWidget(self.widget)
        #adding some fixed Space stuff will take
        self.QVBoxLayout.setSpacing(20)
        self.add_url.setFixedWidth(900)
        self.add_url.setFixedHeight(200)
        self.add_url_button.setFixedWidth(60)
        self.add_url_button.setFixedHeight(70)
        self.start_DL.setFixedWidth(60)
        self.start_DL.setFixedHeight(70)
        self.user_path_button.setFixedWidth(20)
        self.user_path_button.setFixedHeight(20)

        #setting scrollArea Geometry
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumHeight(400)
        self.scrollArea.setMinimumWidth(600)
        self.scrollArea.setContentsMargins(10, 10, 10, 10)

        #adding jobs to ScrollArea

        # for progress_bar in self.progress_bars:
        #   self.job_container_layout.addWidget(progress_bar,alignment=Qt.AlignTop)

        self.job_container.setLayout(self.job_container_layout)
        self.scrollArea.setWidget(self.job_container)


        #setting object names
        self.widget.setObjectName("main_bg")
        self.label_url.setObjectName("ask_url")
        self.add_url.setObjectName("add_url")
        self.add_url_button.setObjectName("add_url_button")
        self.start_DL.setObjectName("start_dl")
        self.scrollArea.setObjectName("scrollArea")
        self.user_path.setObjectName("user_path")
        self.user_path_button.setObjectName("user_path_button")
        #more object names
        self.job_container.setObjectName("job_container")

        self.setStyleSheet("""
/* ---------- Main window & font ---------- */

#main_bg {
    border-image: url("wallpaper.jpg") 0 0 0 0 round stretch;
    /* subtle default tint so widgets are readable */
    background-color: rgba(40,40,43,0.35);
}

/* ---------- Top label ---------- */
#ask_url {
    color: #cccac4;
    font-size: 30px;
    font-family: Comic Sans MS;
    font-weight: 700;
    padding: 8px 12px;
    border-radius: 11px;
    background-color: #2b2824;
    border: 1px solid #759096;
}

/* ---------- URL input ---------- */
#add_url {
    background-color: rgba(18,18,18,0.72);
    font-size: 30px;
    font-family: Comic Sans MS;
    color: #efefef;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 6px 12px;
    min-height: 34px;
    max-width: 700px;
    selection-background-color: rgba(58,122,254,0.25);
}

#add_url:focus {
    border: 1px solid rgba(58,122,254,0.95);
    background-color: rgba(20,20,21,0.82);
}

/* ---------- Scroll area (download list) ---------- */
#scrollArea {
    background: #42413e;
    border-radius: 12px;
    border: 1px solid #ffc561;
}

/* ---------- User Path input ---------- */
#user_path {
    background-color: rgba(18,18,18,0.72);
    font-size: 20px;
    font-family: Comic Sans MS;
    color: #efefef;
    border: 1px solid #77acb8;
    border-radius: 10px;
    padding: 6px 12px;
    min-height: 34px;
    max-width: 700px;
    selection-background-color: rgba(58,122,254,0.25);
}

#user_path:focus {
    border: 1px solid rgba(58,122,254,0.95);
    background-color: rgba(20,20,21,0.82);
}

/* ---------- ADD Download button ---------- */
#add_url_button {
    color: #ffffff;
    font-size: 30px;
    font-family: Comic Sans MS;
    color: #efefef;
    border: 1px solid #77acb8;
    border-radius: 10px;
    padding: 8px 16px;
    min-height: 40px;
    max-width: 700px;
    selection-background-color: #77acb8;
}

#add_url_button:hover {
    background-color: #827f79;
}

#add_url_button:pressed {
    background-color: #5e5d5a;
}

/* ---------- Start Download button ---------- */
#start_dl {
    color: #ffffff;
    font-size: 32px;
    font-family: Comic Sans MS;
    color: #efefef;
    border: 1px solid #77acb8;
    border-radius: 10px;
    padding: 8px 16px;
    min-height: 40px;
    max-width: 700px;
    selection-background-color: #77acb8;
}

#start_dl:hover {
    background-color: #827f79;
}

#start_dl:pressed {
    background-color: #5e5d5a;
}

/* ---------- User Path button ---------- */
#user_path_button {
    color: #ffffff;
    font-size: 20px;
    font-family: Comic Sans MS;
    color: #efefef;
    border: 1px solid #77acb8;
    border-radius: 10px;
    padding: 6px 12px;
    min-height: 34px;
    max-width: 700px;
    selection-background-color: #77acb8;
}

#user_path_button:hover {
    background-color: #827f79;
}

#user_path_button:pressed {
    background-color: #5e5d5a;
}
/* ---------- Job Container ---------- */

#job_container {

    background: #42413e;
    border-radius: 12px;
}

/* ---------- Progress Bars ---------- */

QProgressBar {
    border: 1px solid #2e3136;
    border-radius: 8px;
    background-color: #2a2927;
    color: #f0f0f0;
    font-family: Comic Sans MS;
    font-size: 14px;
    text-align: center;
    min-height: 22px;
}

/* The filled part */
QProgressBar::chunk {
    border-radius: 8px;
    background-color: #77acb8;           /* base color */
    /* optional subtle gradient vibe */
    background-image: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0  #5ab1c7,
        stop:0.5 #77acb8,
        stop:1  #94c0cc
    );
    margin: 1px;                         /* small inner padding */
}

""")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadManager()
    window.show()
    sys.exit(app.exec_())
