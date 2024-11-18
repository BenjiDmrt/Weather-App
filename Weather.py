import sys

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QCheckBox, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5 import QtGui

class wheaterapp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(600, 300, 400, 450)
        self.setWindowIcon(QtGui.QIcon("C:/Users/aquar/Downloads/icon.png"))
        self.city_name = QLabel("Enter city name:", self)
        self.input_ = QLineEdit(self)
        self.get_weather = QPushButton("Get Weather", self)
        self.temp = QLabel(self)
        self.emoji = QLabel(self)
        self.condition = QLabel(self)
        self.error = QLabel(self)
        self.iniUI()
    def iniUI(self):


        vbox = QVBoxLayout()
        vbox.addWidget(self.city_name)
        vbox.addWidget(self.input_)
        vbox.addWidget(self.get_weather)
        vbox.addWidget(self.temp)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.condition)
        vbox.addWidget(self.error)

        self.setLayout(vbox)

        self.city_name.setAlignment(Qt.AlignCenter)
        self.input_.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.condition.setAlignment(Qt.AlignCenter)
        self.error.setAlignment(Qt.AlignTop)

        self.city_name.setObjectName("city_name")
        self.input_.setObjectName("input_")
        self.get_weather.setObjectName("get_weather")
        self.temp.setObjectName("temp")
        self.emoji.setObjectName("emoji")
        self.condition.setObjectName("condition")
        self.error.setObjectName("error")

        self.setStyleSheet("""
            QLabel#city_name{
                font-size:40px;
            }
            QLineEdit#input_{
                font-size:40px;
            }
            QPushButton#get_weather{
                font-size:30px;
            }
            QLabel#temp{
                font-size:50px;
            }
            QLabel#temp{
                font-size:40px;
            }
            QLabel#emoji{
                font-size:50px;

            }
            QLabel#condition{
                font-size:30px;
            }
            QLabel#error{
                font-size: 40px;
            }
         """)

        self.get_weather.clicked.connect(self.apiweather)
    def apiweather(self):
        city = self.input_.text()
        api_key = "**enter api key**"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            request = requests.get(url)
            request.raise_for_status()
            data = request.json()
            if request.status_code == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match request.status_code:
                case 400:
                    self.errors("Bad Request")
                case 401:
                    self.errors("Unauthorized access")
                case 402:
                    self.errors("Payment required")
                case 403:
                    self.errors("Forbidden access")
                case 404:
                    self.errors("Not Found:\nCity not found")
                case 500:
                    self.errors("Forbidden access")
                case 501:
                    self.errors("Not Implemented")
                case 502:
                    self.errors("Bad Gateaway")
                case 503:
                    self.errors("Service Unavailable")
                case 504:
                    self.errors("Gateaway Timeout")
        except requests.exceptions.ConnectionError:
            self.errors("Connection Error")
        except requests.exceptions.Timeout:
            self.errors("Timeout Error")
        except requests.exceptions.TooManyRedirects:
            self.errors("Too many Redirects")
        except requests.exceptions.RequestException as req_error:
            self.errors("Request Error")
    def errors(self, message):
        self.temp.setStyleSheet("font-size:30px;")
        self.emoji.setText("")
        self.condition.setText("")
        self.temp.setText(message)

    def display_weather(self, data):

        temp = data['main']['temp']
        tempc = round(temp - 273.15, 1)
        tempc = str(tempc)
        description = data['weather'][0]['description']
        id = data['weather'][0]['id']
        self.temp.setText(f"{tempc}°C")
        self.condition.setText(description)
        self.emoji.setText(self.get_emoji(id))


    def get_emoji(self, id):
        if 200 <= id <= 232:
            return "⛈️"
        elif 300 <= id <= 321:
            return "🌦️"
        elif 500 <= id <= 531:
            return "🌦️"
        elif 600 <= id <= 622:
            return "🌨️"
        elif 701 <= id <= 771:
            return "🌫️"
        elif id == 781:
            return "🌪️"
        elif id == 800:
            return "☀️"
        elif 801 <= id <= 804:
            return "☁️"
        else:
            return ""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = wheaterapp()
    window.show()
    sys.exit(app.exec_())
