# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EventWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.Control import (DateTimeEdit, LabelImage, RelationalComboBox)
from App.Widget.View import EnhancedTableView

class Ui_EventWidget(object):
    def setupUi(self, EventWidget):
        if not EventWidget.objectName():
            EventWidget.setObjectName(u"EventWidget")
        EventWidget.resize(919, 602)
        self.verticalLayout = QVBoxLayout(EventWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(EventWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_15 = QVBoxLayout(self.page1)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.groupBox_2 = QGroupBox(self.page1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lineEditDescription = QLineEdit(self.groupBox_2)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.verticalLayout_3.addWidget(self.lineEditDescription)


        self.verticalLayout_14.addWidget(self.groupBox_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.dateTimeEditStart = DateTimeEdit(self.groupBox_3)
        self.dateTimeEditStart.setObjectName(u"dateTimeEditStart")
        self.dateTimeEditStart.setEnabled(True)
        self.dateTimeEditStart.setMinimumDate(QDate(1800, 1, 1))
        self.dateTimeEditStart.setCalendarPopup(True)

        self.verticalLayout_5.addWidget(self.dateTimeEditStart)


        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.page1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.dateTimeEditEnd = DateTimeEdit(self.groupBox_4)
        self.dateTimeEditEnd.setObjectName(u"dateTimeEditEnd")
        self.dateTimeEditEnd.setMinimumDate(QDate(1800, 1, 1))
        self.dateTimeEditEnd.setCalendarPopup(True)

        self.verticalLayout_6.addWidget(self.dateTimeEditEnd)


        self.horizontalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.page1)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.comboBoxPriceList = RelationalComboBox(self.groupBox_5)
        self.comboBoxPriceList.setObjectName(u"comboBoxPriceList")

        self.verticalLayout_10.addWidget(self.comboBoxPriceList)


        self.horizontalLayout_2.addWidget(self.groupBox_5)


        self.verticalLayout_14.addLayout(self.horizontalLayout_2)

        self.labelEventUsed = QLabel(self.page1)
        self.labelEventUsed.setObjectName(u"labelEventUsed")
        font = QFont()
        font.setBold(True)
        self.labelEventUsed.setFont(font)
        self.labelEventUsed.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayout_14.addWidget(self.labelEventUsed)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_2)


        self.horizontalLayout_6.addLayout(self.verticalLayout_14)

        self.groupBox = QGroupBox(self.page1)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelEventImage = LabelImage(self.groupBox)
        self.labelEventImage.setObjectName(u"labelEventImage")
        self.labelEventImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelEventImage.setProperty(u"hasImage", True)

        self.verticalLayout_2.addWidget(self.labelEventImage)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonUpload = QPushButton(self.groupBox)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.horizontalLayout.addWidget(self.pushButtonUpload)

        self.pushButtonDownload = QPushButton(self.groupBox)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout.addWidget(self.pushButtonDownload)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonDelete = QPushButton(self.groupBox)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout.addWidget(self.pushButtonDelete)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_9.addLayout(self.verticalLayout_2)


        self.horizontalLayout_6.addWidget(self.groupBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_7 = QVBoxLayout(self.page2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_7.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout.addWidget(self.stackedWidget)

        QWidget.setTabOrder(self.lineEditDescription, self.dateTimeEditStart)
        QWidget.setTabOrder(self.dateTimeEditStart, self.dateTimeEditEnd)
        QWidget.setTabOrder(self.dateTimeEditEnd, self.pushButtonUpload)
        QWidget.setTabOrder(self.pushButtonUpload, self.pushButtonDownload)
        QWidget.setTabOrder(self.pushButtonDownload, self.pushButtonDelete)
        QWidget.setTabOrder(self.pushButtonDelete, self.tableView)

        self.retranslateUi(EventWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(EventWidget)
    # setupUi

    def retranslateUi(self, EventWidget):
        EventWidget.setWindowTitle(QCoreApplication.translate("EventWidget", u"Event", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("EventWidget", u"Event description", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("EventWidget", u"Start date", None))
        self.dateTimeEditStart.setSpecialValueText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("EventWidget", u"End date", None))
        self.dateTimeEditEnd.setSpecialValueText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("EventWidget", u"Price list", None))
        self.labelEventUsed.setText(QCoreApplication.translate("EventWidget", u"This event is used, dates can't be changed", None))
        self.groupBox.setTitle(QCoreApplication.translate("EventWidget", u"Event image", None))
        self.labelEventImage.setText(QCoreApplication.translate("EventWidget", u"NO IMAGE", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("EventWidget", u"Upload...", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("EventWidget", u"Download...", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("EventWidget", u"Delete", None))
    # retranslateUi

