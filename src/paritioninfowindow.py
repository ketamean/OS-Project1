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
    QLabel, QProgressBar, QSizePolicy, QTreeWidget,
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
        __qtreewidgetitem1 = QTreeWidgetItem(self.tw_directory)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        self.tw_directory.setObjectName(u"tw_directory")
        self.tw_directory.setGeometry(QRect(40, 100, 256, 361))
        font1 = QFont()
        font1.setFamilies([u"Outfit"])
        font1.setPointSize(15)
        self.tw_directory.setFont(font1)
        self.tw_directory.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;")
        self.lb_partionInfo = QLabel(self.groupBox)
        self.lb_partionInfo.setObjectName(u"lb_partionInfo")
        self.lb_partionInfo.setGeometry(QRect(350, 100, 511, 361))
        self.lb_partionInfo.setFont(font1)
        self.lb_partionInfo.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);\n"
"padding: 15px;")
        self.pb_diskUsage = QProgressBar(self.groupBox)
        self.pb_diskUsage.setObjectName(u"pb_diskUsage")
        self.pb_diskUsage.setGeometry(QRect(380, 400, 451, 21))
        self.pb_diskUsage.setAutoFillBackground(False)
        self.pb_diskUsage.setStyleSheet(u"border-radius: 4px")
        self.pb_diskUsage.setValue(24)
        self.pb_diskUsage.setTextVisible(False)
        self.lb_info = QLabel(self.groupBox)
        self.lb_info.setObjectName(u"lb_info")
        self.lb_info.setGeometry(QRect(350, 560, 511, 131))
        self.lb_info.setFont(font1)
        self.lb_info.setStyleSheet(u"background-color: rgb(68, 64, 61);\n"
"border-radius: 30px;\n"
"color: rgb(255, 255, 255);\n"
"padding: 15px;")

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

        __sortingEnabled = self.tw_directory.isSortingEnabled()
        self.tw_directory.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.tw_directory.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Partion_Window", u"Folder A", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Partion_Window", u"New Subitem", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Partion_Window", u"New Item", None));
        self.tw_directory.setSortingEnabled(__sortingEnabled)

        self.lb_partionInfo.setText(QCoreApplication.translate("Partion_Window", u"This is where text show", None))
        self.lb_info.setText(QCoreApplication.translate("Partion_Window", u"TextLabel", None))
    # retranslateUi

