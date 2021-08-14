import sys

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QPushButton


class MainWindow(QDialog):
    """
    Главное окно программы
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Timer')
        self.setGeometry(20, 50, 400, 250)
        self.setStyleSheet('background-color: #2c2c2c;')

        self.timer_label = QLabel(self)
        self.timer_label.setGeometry(100, 50, 200, 50)
        self.timer_label.setText('0:00:00')
        self.timer_label.setStyleSheet('border: 2px solid #fff; color: #fff; font-size: 20px;')
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton(self)
        self.start_button.setGeometry(150, 150, 100, 45)
        self.start_button.setStyleSheet("""outline: none; background-color: #fff; color: #2c2c2c;
                                            font-size: 18px;""")
        self.start_button.setText('СТАРТ')
        self.start_button.clicked.connect(self.start_timer)

        self.pause_button = QPushButton(self)
        self.pause_button.setGeometry(66, 150, 100, 45)
        self.pause_button.setStyleSheet("""outline: none; background-color: #fff; color: #2c2c2c;
                                                    font-size: 18px;""")
        self.pause_button.setText('ПАУЗА')
        self.pause_button.hide()
        self.pause_button.clicked.connect(self.pause_timer)

        self.stop_button = QPushButton(self)
        self.stop_button.setGeometry(232, 150, 100, 45)
        self.stop_button.setStyleSheet("""outline: none; background-color: #fff; color: #2c2c2c;
                                                            font-size: 18px;""")
        self.stop_button.setText('СТОП')
        self.stop_button.hide()
        self.stop_button.clicked.connect(self.stop_timer)

        self.thread_timer = QtCore.QThread()
        self.stop_watch = StopWatch()
        self.stop_watch.moveToThread(self.thread_timer)
        self.stop_watch.sec_commit.connect(self.change_sec)
        self.thread_timer.started.connect(self.stop_watch.run)

    def pause_timer(self):
        button_text = self.pause_button.text()
        if button_text == 'ВОЗОБНОВИТЬ':
            self.pause_button.setGeometry(66, 150, 100, 45)
            self.pause_button.setText('ПАУЗА')
            self.stop_watch.pause = False

        else:
            self.pause_button.setGeometry(66, 150, 150, 45)
            self.pause_button.setText('ВОЗОБНОВИТЬ')
            self.stop_watch.pause = True

    def stop_timer(self):
        self.stop_watch.running = False
        self.timer_label.setText('0:00:00')
        self.pause_button.hide()
        self.stop_button.hide()
        self.start_button.show()

    def show_main_window(self):
        self.show()

    def start_timer(self):
        self.stop_watch.running = True
        self.start_button.hide()
        self.pause_button.show()
        self.stop_button.show()
        self.pause_button.setText('ПАУЗА')
        self.stop_watch.pause = False
        self.thread_timer.start()

    @QtCore.pyqtSlot(str)
    def change_sec(self, seconds):
        hours, minutes, seconds = self.calculate_time(seconds)
        self.timer_label.setText(f'{hours}:{minutes}:{seconds}')

    def calculate_time(self, seconds):
        hours = '00'
        minutes = '00'

        if int(seconds) >= 3600:
            hours = int(seconds) // 3600
            seconds = int(seconds) - hours * 3600
            if hours < 10:
                hours = f'0{hours}'

        elif int(seconds) >= 60:
            minutes = int(seconds) // 60
            seconds = int(seconds) - minutes * 60
            if minutes < 10:
                minutes = f'0{minutes}'

        if int(seconds) < 10:
            seconds = f'0{seconds}'

        return hours, minutes, seconds


class StopWatch(QtCore.QObject):
    running = True
    sec_commit = QtCore.pyqtSignal(str)
    pause = False

    def run(self):
        sec = 0
        while True:
            if not self.running:
                sec = 0
                continue
            if self.pause:
                continue
            QtCore.QThread.msleep(1000)
            sec += 1
            self.sec_commit.emit(str(sec))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show_main_window()
    sys.exit(app.exec_())
