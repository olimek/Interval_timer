import sys
from sys import exit
from os import system, name
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QPushButton, QRadioButton, QLCDNumber, QLabel, QFrame, QLineEdit
from PySide6.QtCore import QFile, QObject, QTimer
from random import seed
from random import randint
import time
import os
import pygame

DEFAULT_SET = 100
DEFAULT_PAR = 2
DEFAULT_DEL = 2
DEFAULT_RDEL = 3.5


class Form(QObject):
    def __init__(self, ui_file="GUI.ui", parent=None):
        super(Form, self).__init__(parent)
        pygame.init()
        pygame.mixer.init()
        self.digit = 0
        self.DEFAULT_SET = DEFAULT_SET
        self.DEFAULT_PAR = DEFAULT_PAR
        self.DEFAULT_DEL = DEFAULT_DEL
        self.DEFAULT_RDEL = DEFAULT_RDEL
        self.tt = 00
        self.set = 0
        self.STATEMENT = "STOP"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateScreen)
        self.timer.start(1)
        self.script_dir = os.path.dirname(__file__)
        ui_file = QFile(self.script_dir + "/" + ui_file)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.widget = loader.load(ui_file)
        ui_file.close()

        # Button
        self.START_Button = self.widget.findChild(QPushButton, "pushButton_Start")
        self.STOP_Button = self.widget.findChild(QPushButton, "pushButton_Stop")

        # Display
        self.LCD = self.widget.findChild(QLCDNumber, "lcdNumber_M1")

        self.label = self.widget.findChild(QLabel, "label_3")
        self.Frame = self.widget.findChild(QFrame, "frame")

        self.Sets_Text = self.widget.findChild(QLineEdit, "lineEdit_Sets")
        self.Par_Text = self.widget.findChild(QLineEdit, "lineEdit_Par")
        self.Del_Text = self.widget.findChild(QLineEdit, "lineEdit_Delay")
        self.Rand_Text = self.widget.findChild(QLineEdit, "lineEdit_RandomDelay")
        self.Rand_Radio = self.widget.findChild(QRadioButton, "radioButton_Random")

        # Action
        self.START_Button.clicked.connect(self.ClickedSTARTButton)
        self.STOP_Button.clicked.connect(self.ClickedSTOPButton)

        self.Rand_Radio.toggled.connect(self.ClickedRadioBox)

        self.LCD.display("00:00.000")
        self.Sets_Text.setText(str(self.DEFAULT_SET))
        self.Par_Text.setText(str(self.DEFAULT_PAR))
        self.Del_Text.setText(str(self.DEFAULT_DEL))

    def ClickedRadioBox(self):
        self.Rand_Text.setEnabled(self.Rand_Radio.isChecked())

    def ClickedSTARTButton(self):
        if self.Rand_Text.text() == "0":
            RAND = self.Del_Text.text()
        else:
            if float(self.Rand_Text.text().replace(",", ".")) < float(self.Del_Text.text().replace(",", ".")):
                RAND = self.Del_Text.text()
            else:
                RAND = self.Rand_Text.text()

        self.DEFAULT_RDEL = float(RAND.replace(",", "."))
        self.DEFAULT_DEL = float(self.Del_Text.text().replace(",", "."))
        self.DEFAULT_PAR = float(self.Par_Text.text().replace(",", "."))
        self.DEFAULT_SET = int(self.Sets_Text.text())

        self.STATEMENT = "run"
        self.Run(self.DEFAULT_PAR, self.DEFAULT_DEL, self.DEFAULT_RDEL, self.DEFAULT_SET)

    def ClickedSTOPButton(self):
        if self.STATEMENT == "run":
            self.STATEMENT = "Pause"
        elif self.STATEMENT == "Pause":
            self.STATEMENT = "stop"

    def current_milli_time(self):
        return round(time.time() * 1000)

    def convertMillis(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24
        millis = millis % 1000

        self.LCD.display(str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(millis).zfill(3))
        if self.STATEMENT == "run":
            self.Sets_Text.setText(str(self.set))
        elif self.STATEMENT == "Pause":
            self.Sets_Text.setText(str(self.set))
        elif self.STATEMENT == "stop":
            self.LCD.display("00:00.000")

            self.Frame.setStyleSheet("background-color: rgba(0, 0, 0,0);")

    def UpdateScreen(self):
        self.convertMillis(self.tt)

    def clear(self):
        system("cls")
        os.system("cls")

    def Run(self, PARms, DELms, RDELms, SET):
        if (DELms <= 0):
            DELms = RDELms = 3

        seed(1)
        flag = True
        self.Rdelms = randint(DELms*10, RDELms*10)*100
        self.tt = randint(DELms*10, RDELms*10)*100
        self.Frame.setStyleSheet("background-color: rgba(255, 20, 71,150);")  # RED
        ct = self.current_milli_time()
        cct = self.current_milli_time()
      
        self.set = SET
        



        while (self.set >= 0) and (self.STATEMENT == "run"):

            self.clear()
            print("SET  " + str(self.set))
            print(randint(DELms*10, RDELms*10)*100)

            if flag:
                print("Break")
            else:
                self.clear()
                print("Work")
            while True and (self.STATEMENT == "run"):
                app.processEvents()

                if (self.current_milli_time() - cct >= 1):
                    cct = self.current_milli_time()
                    self.tt -= 1


                if (self.current_milli_time() - ct >= (self.Rdelms)):
                    ct = self.current_milli_time()
                    break



            sound = pygame.mixer.Sound(file='time.wav')
            sound.play(loops=0)

            if flag:
                self.Rdelms = PARms*1000
                self.tt = PARms*1000
                self.Frame.setStyleSheet("background-color: rgba(80, 255, 102,150);")  # Green
                if self.set == 0:
                    self.set -= 1
                flag = False
            else:
                if self.set >0:
                    self.Rdelms = randint(DELms*10, RDELms*10)*100
                    self.tt = randint(DELms*10, RDELms*10)*100
                    self.Frame.setStyleSheet("background-color: rgba(255, 20, 71,150);")  # RED
                    if self.set > 0:
                        self.set -= 1
                    flag = True

            
            if self.set < 0 :
                self.STATEMENT="stop"
                self.LCD.display('00:00.000')
                self.Frame.setStyleSheet("background-color: rgba(0, 0, 0,0);")



if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QGridLayout, QWidget

    app = QApplication(sys.argv)
    form = Form()
    mainWidget = QWidget()
    mainWidget.setWindowTitle("ShootingIntevealTimer")
    layout = QGridLayout()
    layout.addWidget(form.widget, 0, 0)

    mainWidget.setLayout(layout)
    mainWidget.setMinimumSize(930, 560)
    mainWidget.adjustSize()

    mainWidget.show()

    mainWidget.raise_()
    exit(app.exec_())
