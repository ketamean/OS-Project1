# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(923, 715)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"background-color: rgb(35, 30, 27);")
        self.lb_introduction = QLabel(self.groupBox)
        self.lb_introduction.setObjectName(u"lb_introduction")
        self.lb_introduction.setGeometry(QRect(10, 493, 891, 151))
        font = QFont()
        font.setFamilies([u"Outfit"])
        font.setPointSize(15)
        self.lb_introduction.setFont(font)
        self.lb_introduction.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_volumeTitle = QLabel(self.groupBox)
        self.lb_volumeTitle.setObjectName(u"lb_volumeTitle")
        self.lb_volumeTitle.setGeometry(QRect(110, 40, 111, 43))
        font1 = QFont()
        font1.setFamilies([u"Outfit"])
        font1.setPointSize(24)
        font1.setBold(False)
        self.lb_volumeTitle.setFont(font1)
        self.lb_volumeTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_appFeaturesTitle = QLabel(self.groupBox)
        self.lb_appFeaturesTitle.setObjectName(u"lb_appFeaturesTitle")
        self.lb_appFeaturesTitle.setGeometry(QRect(370, 40, 301, 43))
        self.lb_appFeaturesTitle.setFont(font1)
        self.lb_appFeaturesTitle.setLayoutDirection(Qt.LeftToRight)
        self.lb_appFeaturesTitle.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lb_appFeaturesTitle.setAlignment(Qt.AlignCenter)
        self.lb_appFeatures = QLabel(self.groupBox)
        self.lb_appFeatures.setObjectName(u"lb_appFeatures")
        self.lb_appFeatures.setGeometry(QRect(350, 100, 511, 361))
        self.lb_appFeatures.setFont(font)
        self.lb_appFeatures.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);\n"
"padding: 15px;")
        self.list_volume = QListWidget(self.groupBox)
        self.list_volume.setObjectName(u"list_volume")
        self.list_volume.setGeometry(QRect(40, 100, 256, 361))
        self.list_volume.setFont(font)
        self.list_volume.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"padding: 15px;\n"
"color: rgb(255, 255, 255);")

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 923, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Operating System - Disk Management Application", None))
        self.groupBox.setTitle("")
        self.lb_introduction.setText(QCoreApplication.translate("MainWindow", u"Group Members:", None))
        self.lb_volumeTitle.setText(QCoreApplication.translate("MainWindow", u"Volume", None))
        self.lb_appFeaturesTitle.setText(QCoreApplication.translate("MainWindow", u"Application Features", None))
        self.lb_appFeatures.setText(QCoreApplication.translate("MainWindow", u"This is where text show", None))
    # retranslateUi

