from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QVBoxLayout, QDialog, QGroupBox,
                             QGridLayout, QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5 import QtWidgets
import sys, os
#import client, P2PClient, P2PServer


class dataGallery(QDialog):
    def __init__(self, parent=None, debug=False):
        super(dataGallery, self).__init__(parent)
        self.debug = debug # Show print statements in the console
        self.server = None
        self.certificateName = None

        self.createTopLeftLogIn()
        self.createBottomLeftButtons()
        self.createRightTable()
        self.createRightStreamBox()
        self.createBottomCertButton()

        layout = QGridLayout()
        layout2 = QVBoxLayout()

        layout.addWidget(self.topLeftGroupBox, 0, 0)
        layout.addWidget(self.bottomLeftGroupBox, 1, 0)
        layout.addWidget(self.rightGroupBox, 0, 1)
        layout.addWidget(self.bottomRightGroupBox, 1, 1)

        layout2.addLayout(layout)
        layout2.addWidget(self.certificateButton)

        self.setLayout(layout2)

        self.setWindowTitle('P2P Host')

    def createTopLeftLogIn(self):
        self.topLeftGroupBox = QGroupBox('Log In')

        self.usernameBox = QLineEdit(self)
        self.usernameBox.setStyleSheet("color: black")
        self.usernameBox.setPlaceholderText('username')

        self.addressBox = QLineEdit(self)
        self.addressBox.setStyleSheet("color: black")
        self.addressBox.setPlaceholderText('127.0.0.1')

        self.sslBox = QLineEdit(self)
        self.sslBox.setStyleSheet("color: black")
        self.sslBox.setPlaceholderText('host.name')

        self.personalAddressBox = QLineEdit(self)
        self.personalAddressBox.setStyleSheet("color: black")
        self.personalAddressBox.setPlaceholderText('personal address')

        layout = QVBoxLayout()
        layout.addWidget(self.usernameBox)
        layout.addWidget(self.addressBox)
        layout.addWidget(self.sslBox)
        layout.addWidget(self.personalAddressBox)

        self.topLeftGroupBox.setLayout(layout)

    def createBottomLeftButtons(self):
        self.bottomLeftGroupBox = QGroupBox()

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.button_connect)

        self.disconnectButton = QPushButton('Disconnect')
        self.disconnectButton.setEnabled(False)
        self.disconnectButton.clicked.connect(self.button_disconnect)

        self.refreshButton = QPushButton('Refresh')
        self.refreshButton.setEnabled(False)
        self.refreshButton.clicked.connect(self.button_refresh)

        self.streamButton = QPushButton('Stream')
        self.streamButton.setEnabled(False)
        self.streamButton.clicked.connect(self.button_stream)

        layout = QGridLayout()
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 6)

        layout.addWidget(self.connectButton, 0, 0)
        layout.addWidget(self.disconnectButton, 1, 0)
        layout.addWidget(self.refreshButton, 0, 1)
        layout.addWidget(self.streamButton, 1, 1)

        self.bottomLeftGroupBox.setLayout(layout)


    def createRightTable(self):
        self.rightGroupBox = QGroupBox('Table')

        self.tableWidget = QTableWidget(2, 2)
        self.tableWidget.setStyleSheet("color: black")

        self.header_labels = ['Username', 'Address']
        self.tableWidget.setHorizontalHeaderLabels(self.header_labels)
        self.tableWidget.setVerticalHeaderLabels(('', ''))
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.move(0,0)

        layout = QHBoxLayout()

        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.tableWidget)

        self.rightGroupBox.setLayout(layout)

    def createRightStreamBox(self):
        self.bottomRightGroupBox = QGroupBox('Streaming Service')

        label = QLabel('Selected address')

        self.slctAddressBox = QLineEdit(self)
        self.slctAddressBox.setStyleSheet('color: black')
        self.slctAddressBox.setEnabled(False)

        self.watchButton = QPushButton('Watch')
        self.watchButton.setEnabled(False)
        self.watchButton.clicked.connect(self.button_watch)

        layout = QVBoxLayout()

        layout.addWidget(label)
        layout.addWidget(self.slctAddressBox)
        layout.addWidget(self.watchButton)

        self.bottomRightGroupBox.setLayout(layout)

    def createVideoBox(self):
        self.topVideoBox = QGroupBox('Player')
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

        self.topVideoBox.setLayout(layout)

    def createBottomCertButton(self):
        self.certificateButton = QPushButton('Certificate location')
        self.certificateButton.clicked.connect(self.button_certificate)

        """layout = QVBoxLayout()

        layout.addWidget(self.certificateButton)"""

    def button_connect(self):
        usernameValue = self.usernameBox.text()

        if len(usernameValue) > 0:
            addressValue = self.addressBox.text()
            hostnameValue = self.sslBox.text()
            self.client = client.Client(usernameValue, self, addressValue, hostname=hostnameValue, debug=self.debug, certlocation=self.certificateName)
            try:
                self.client.cnct(addressValue)
            except:
                self.errorDialogBox("Error in connecting to the server!")
            else:
                self.disconnectButton.setEnabled(True)
                self.refreshButton.setEnabled(True)
                self.streamButton.setEnabled(True)
                self.connectButton.setEnabled(False)

    def button_disconnect(self, error=False):
        if not error:
            self.client.command('close')
        if self.server is not None:
            self.server.stopConnection()
        self.connectButton.setEnabled(True)
        self.disconnectButton.setEnabled(False)
        self.refreshButton.setEnabled(False)
        self.streamButton.setEnabled(False)
        self.watchButton.setEnabled(False)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(2)

    def button_refresh(self):
        try:
            table = self.client.load()
        except: # Handles both broken pipe and conn. reset, and others that I might not know
            self.errorDialogBox('The server interrupted the connection.')
            self.button_disconnect(True)
        else:
            self.tableWidget.setRowCount(0)

            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(self.header_labels)
            keys = list(table)
            for rowIndex in range(len(table)):
                self.tableWidget.insertRow(rowIndex)
                key = keys[rowIndex]
                userName = QTableWidgetItem(key)
                userName.setFlags(Qt.ItemIsEnabled)

                address = QTableWidgetItem(table[key])
                address.setFlags(Qt.ItemIsEnabled)

                self.tableWidget.setItem(rowIndex, 0, userName)
                self.tableWidget.setItem(rowIndex, 1, address)

    def button_stream(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Stream",
                                                  QDir.homePath())
        if fileName != '':
            address = self.personalAddressBox.text()
            if address == '':
                try:
                    self.client.stream()
                except UserWarning:
                    self.errorDialogBox('The username is already in use')
                except:
                    self.errorDialogBox('The server interrupted the connection.')
                    self.button_disconnect(True)
                else:
                    self.server = P2PServer.P2PServer(fileName, debug=self.debug)
            else:
                try:
                    self.client.stream(address)
                except UserWarning:
                    self.errorDialogBox('The username is already in use')
                except:
                    self.errorDialogBox('The server interrupted the connection.')
                    self.button_disconnect(True)
                else:
                    self.server = P2PServer.P2PServer(fileName, address=address, debug=self.debug)

    def button_watch(self):
        ip = self.slctAddressBox.text()
        self.watchButton.setEnabled(False)
        self.slctAddressBox.setText('')
        self.p2pclient = P2PClient.P2PClient(ip, debug=self.debug)
        self.p2pclient.run()

    def button_certificate(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Stream",
                                                  './')
        if fileName != '':
            self.certificateName = fileName

    def on_click(self):
        item = self.tableWidget.currentItem()
        if item is not None:
            col = item.column()
            row = item.row()
            item = self.tableWidget.item(row, 1)  # Always take the IP
            if self.debug:
                print(row, col)
            if item is not None:
                self.slctAddressBox.setText(item.text())
                if not self.watchButton.isEnabled():
                    self.watchButton.setEnabled(True)
            else:
                self.errorDialogBox('There is no IP entry in this row')
        else:
            self.errorDialogBox('There is no value in the selected cell')

    def errorDialogBox(self, message):
        alert = QMessageBox(self)
        alert.setText(message)
        alert.exec_()


if __name__ == '__main__':
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setStyle('fusion')
    gallery = dataGallery()
    gallery.show()
    # os instead of sys to kill the instance of the interpreter to stop underlying sockets
    os._exit(app.exec_())