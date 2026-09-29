from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QPushButton,
                               QVBoxLayout, QWidget, QTextBrowser, QLabel)


class Ui_MainWindow(object):
    """Класс из Qt Designer для инициализации графического интерфейса"""
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.out_window = QTextBrowser(self.centralwidget)
        self.out_window.setObjectName(u"out_window")

        self.verticalLayout.addWidget(self.out_window)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.cmd_promt = QLabel()
        self.cmd_promt.setObjectName(u"prefix_text")
        self.horizontalLayout.addWidget(self.cmd_promt)

        self.cmd_line = QLineEdit(self.centralwidget)
        self.cmd_line.setObjectName(u"cmd_line")

        self.horizontalLayout.addWidget(self.cmd_line)

        self.enter_btn = QPushButton(self.centralwidget)
        self.enter_btn.setObjectName(u"enter_button")

        self.horizontalLayout.addWidget(self.enter_btn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.enter_btn.setText(
            QCoreApplication.translate("MainWindow", u"Enter", None))
