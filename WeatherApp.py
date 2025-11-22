import requests
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QPushButton,QLineEdit,QWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(400, 300, 700, 700)
        self.label_ask = QLabel("Enter The City Name")
        self.button_submit = QPushButton("Submit")
        self.label_description = QLabel("Sunny")
        self.label_cloud = QLabel("️🌤")
        self.line_city = QLineEdit()
        self.label_temp = QLabel("30°C")
        self.initUI()
        self.button_submit.clicked.connect(self.fetch_request)



    def fetch_request(self):
        api = ""
        city_name = self.line_city.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api}"
        ICON_MAP = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌁",
            "Smoke": "💨",
            "Dust": "🌪️",
        }

        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            result = data

        except requests.exceptions.ConnectTimeout as e:
            self.label_description.setText("Connection Timeout")
            self.label_temp.setText("error")
            print(e)

        except requests.exceptions.ConnectionError as e:
            self.label_description.setText("Connection Error")
            self.label_temp.setText("error")
            print(e)

        except requests.exceptions.HTTPError as e:
            self.label_description.setText("Server returned error")
            self.label_temp.setText("error")
            print(e)

        except Exception as e:
            self.label_description.setText("Exception Occurred")
            self.label_temp.setText("error")
            print(e)

        try:
            cod = int(result['cod'])
        except TypeError, ValueError:
            cod = 0
        try:
             if cod == 200:
                   kelvin = result['main']['temp']
                   celcius = kelvin - 273.15
                   desc = result['weather'][0].get('main')
                   icon = ICON_MAP.get(desc,"❓")
                   self.label_description.setText(desc)
                   self.label_temp.setText(f"{celcius:.1f}°C")
                   self.label_cloud.setText(icon)

             elif cod == 400:
                 self.label_temp.setText(f"{result['cod']}")
                 self.label_description.setText(result['message'])

             elif cod == 404:
                 self.label_temp.setText(f"{result['cod']}")
                 self.label_description.setText(result['message'])

             elif cod == 401:
                 self.label_temp.setText(f"{result['cod']}")
                 self.label_description.setText(result['message'])

             else:
                 self.label_temp.setText("Error")
                 self.label_description.setText(result['message'])


        except Exception:
            print(result)
            self.label_description.setText(result)
            self.label_temp.setText("error")


    def initUI(self):
         self.line_city.setPlaceholderText("Enter it here...")

         self.widget = QWidget()
         self.vbox = QVBoxLayout()
         self.vbox.addWidget(self.label_ask,alignment=Qt.AlignCenter)
         self.vbox.addWidget(self.line_city)
         self.vbox.addWidget(self.button_submit)
         self.vbox.addWidget(self.label_cloud, alignment=Qt.AlignCenter)
         self.vbox.addWidget(self.label_description,alignment=Qt.AlignCenter)
         self.vbox.addWidget(self.label_temp,alignment=Qt.AlignCenter)

         self.widget.setLayout(self.vbox)
         self.setCentralWidget(self.widget)

         self.label_ask.setObjectName("label_ask")
         self.label_temp.setObjectName("label_temp")
         self.label_cloud.setObjectName("label_cloud")
         self.label_description.setObjectName("label_description")


         self.setStyleSheet("""
         
        QWidget{
          background-color: #87CEEB;
          padding: 10px 0px;
          border-radius: 10px solid #87CEEB;
          }
          #label_description {
              color: white;
              font-family: Segoe UI;
              font-size: 40px;
              padding: 6px 12px;
              background-color: rgba(255, 255, 255, 40);
              border-radius: 10px;
          }
        #label_cloud{
          background-color: transparent;
          color: #F3EEE1;             /* soft sky blue emoji tint */
          font-family: Comic Sans MS;
          font-size: 160px;
          padding: 10px 30px;
          border-radius: 30px;        /* fluffy cloud shape */
                                    }
             #label_temp {
          font-family: Comic Sans MS;
          font-size: 40px;
          color: white;
          padding: 14px 100px;
          border-radius: 20px;
          background-color: qlineargradient(
              spread:pad,
              x1:0, y1:0,
              x2:1, y2:1,
              stop:0 #6FB3F2,
              stop:1 #4A8DD8
    );
          border: 3px solid #DDEAFF;
}
        #label_ask{
             font-family: Comic Sans MS;
             font-size: 40px;         
         }
        QLineEdit {
             font-family: Comic Sans MS;
             font-size: 30px;
             padding: 8px;
             border: 2px solid #4A4A4A;
             border-radius: 10px;
             background-color: #F5F5F5;
             color: #000000;
         }

        QPushButton {
             font-family: Comic Sans MS;
             font-size: 40px;
             background-color: #7289DA;
             color: white;
             padding: 10px 18px;
             border-radius: 10px;
             border: none;
         }

        QPushButton:hover {
             background-color: #5B6EAE;
         }

        QPushButton:pressed {
             background-color: #4A5C90;
         }
         """)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
