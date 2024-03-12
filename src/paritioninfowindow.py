# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'paritioninfowindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHeaderView,
    QLabel, QScrollArea, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Partion_Window(object):
    def setupUi(self, Partion_Window):
        if not Partion_Window.objectName():
            Partion_Window.setObjectName(u"Partion_Window")
        Partion_Window.resize(941, 733)
        self.gridLayout = QGridLayout(Partion_Window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Partion_Window)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"background-color: rgb(35, 30, 27);")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 40, 211, 41))
        font = QFont()
        font.setFamilies([u"Outfit"])
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(370, 40, 301, 41))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(370, 500, 181, 41))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.tw_directory = QTreeWidget(self.groupBox)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setBackground(0, QColor(255, 255, 255));
        self.tw_directory.setHeaderItem(__qtreewidgetitem)
        self.tw_directory.setObjectName(u"tw_directory")
        self.tw_directory.setGeometry(QRect(40, 100, 256, 361))
        font1 = QFont()
        font1.setFamilies([u"Outfit"])
        font1.setPointSize(15)
        self.tw_directory.setFont(font1)
        self.tw_directory.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;")
        self.tw_directory.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.lb_partionInfo = QLabel(self.groupBox)
        self.lb_partionInfo.setObjectName(u"lb_partionInfo")
        self.lb_partionInfo.setGeometry(QRect(350, 100, 511, 361))
        font2 = QFont()
        font2.setFamilies([u"Outfit"])
        font2.setPointSize(13)
        self.lb_partionInfo.setFont(font2)
        self.lb_partionInfo.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);\n"
"padding: 15px;")
        self.lb_info = QLabel(self.groupBox)
        self.lb_info.setObjectName(u"lb_info")
        self.lb_info.setGeometry(QRect(350, 560, 511, 131))
        self.lb_info.setFont(font1)
        self.lb_info.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);\n"
"padding: 15px;")
        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(360, 110, 491, 341))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 489, 339))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.tw_directory.raise_()
        self.lb_info.raise_()
        self.scrollArea.raise_()
        self.lb_partionInfo.raise_()

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)


        self.retranslateUi(Partion_Window)

        QMetaObject.connectSlotsByName(Partion_Window)
    # setupUi

    def retranslateUi(self, Partion_Window):
        Partion_Window.setWindowTitle(QCoreApplication.translate("Partion_Window", u"Operating System - Disk Management Application", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Partion_Window", u"Tree Directory", None))
        self.label_2.setText(QCoreApplication.translate("Partion_Window", u"Partition Information", None))
        self.label_3.setText(QCoreApplication.translate("Partion_Window", u"Information", None))
        ___qtreewidgetitem = self.tw_directory.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Partion_Window", u"Folders and Files", None));
        self.lb_partionInfo.setText(QCoreApplication.translate("Partion_Window", u"This is where text show", None))
        self.lb_info.setText(QCoreApplication.translate("Partion_Window", u"TextLabel", None))
    # retranslateUi

