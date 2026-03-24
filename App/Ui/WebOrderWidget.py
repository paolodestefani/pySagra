# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WebOrderWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLCDNumber, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QVBoxLayout,
    QWidget)

from App.Widget.View import EnhancedTableView

class Ui_WebOrderWidget(object):
    def setupUi(self, WebOrderWidget):
        if not WebOrderWidget.objectName():
            WebOrderWidget.setObjectName(u"WebOrderWidget")
        WebOrderWidget.resize(1024, 686)
        self.verticalLayout_2 = QVBoxLayout(WebOrderWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(WebOrderWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.tableViewHeader = EnhancedTableView(self.splitter)
        self.tableViewHeader.setObjectName(u"tableViewHeader")
        self.splitter.addWidget(self.tableViewHeader)
        self.tableViewDetails = EnhancedTableView(self.splitter)
        self.tableViewDetails.setObjectName(u"tableViewDetails")
        self.splitter.addWidget(self.tableViewDetails)

        self.verticalLayout_2.addWidget(self.splitter)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox_4 = QGroupBox(WebOrderWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lcdNumberTotal = QLCDNumber(self.groupBox_4)
        self.lcdNumberTotal.setObjectName(u"lcdNumberTotal")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumberTotal.sizePolicy().hasHeightForWidth())
        self.lcdNumberTotal.setSizePolicy(sizePolicy)
        self.lcdNumberTotal.setMinimumSize(QSize(150, 30))
        self.lcdNumberTotal.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumberTotal.setFrameShadow(QFrame.Shadow.Raised)
        self.lcdNumberTotal.setLineWidth(1)
        self.lcdNumberTotal.setMidLineWidth(0)
        self.lcdNumberTotal.setSmallDecimalPoint(False)
        self.lcdNumberTotal.setDigitCount(10)
        self.lcdNumberTotal.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumberTotal.setProperty(u"value", 999999999.000000000000000)
        self.lcdNumberTotal.setProperty(u"intValue", 999999999)

        self.horizontalLayout_4.addWidget(self.lcdNumberTotal)


        self.horizontalLayout_5.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(WebOrderWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lcdNumberProcessed = QLCDNumber(self.groupBox_3)
        self.lcdNumberProcessed.setObjectName(u"lcdNumberProcessed")
        sizePolicy.setHeightForWidth(self.lcdNumberProcessed.sizePolicy().hasHeightForWidth())
        self.lcdNumberProcessed.setSizePolicy(sizePolicy)
        self.lcdNumberProcessed.setMinimumSize(QSize(150, 30))
        self.lcdNumberProcessed.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumberProcessed.setFrameShadow(QFrame.Shadow.Raised)
        self.lcdNumberProcessed.setLineWidth(1)
        self.lcdNumberProcessed.setMidLineWidth(0)
        self.lcdNumberProcessed.setSmallDecimalPoint(False)
        self.lcdNumberProcessed.setDigitCount(10)
        self.lcdNumberProcessed.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumberProcessed.setProperty(u"value", 999999999.000000000000000)
        self.lcdNumberProcessed.setProperty(u"intValue", 999999999)

        self.horizontalLayout_3.addWidget(self.lcdNumberProcessed)


        self.horizontalLayout_5.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(WebOrderWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lcdNumberUnprocessed = QLCDNumber(self.groupBox)
        self.lcdNumberUnprocessed.setObjectName(u"lcdNumberUnprocessed")
        sizePolicy.setHeightForWidth(self.lcdNumberUnprocessed.sizePolicy().hasHeightForWidth())
        self.lcdNumberUnprocessed.setSizePolicy(sizePolicy)
        self.lcdNumberUnprocessed.setMinimumSize(QSize(150, 30))
        self.lcdNumberUnprocessed.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumberUnprocessed.setFrameShadow(QFrame.Shadow.Raised)
        self.lcdNumberUnprocessed.setLineWidth(1)
        self.lcdNumberUnprocessed.setMidLineWidth(0)
        self.lcdNumberUnprocessed.setSmallDecimalPoint(False)
        self.lcdNumberUnprocessed.setDigitCount(10)
        self.lcdNumberUnprocessed.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumberUnprocessed.setProperty(u"value", 999999999.000000000000000)
        self.lcdNumberUnprocessed.setProperty(u"intValue", 999999999)

        self.horizontalLayout_2.addWidget(self.lcdNumberUnprocessed)


        self.horizontalLayout_5.addWidget(self.groupBox)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.groupBox_2 = QGroupBox(WebOrderWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonDelete = QPushButton(self.groupBox_2)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")

        self.horizontalLayout.addWidget(self.pushButtonDelete)

        self.checkBoxIncludeNotProcessed = QCheckBox(self.groupBox_2)
        self.checkBoxIncludeNotProcessed.setObjectName(u"checkBoxIncludeNotProcessed")

        self.horizontalLayout.addWidget(self.checkBoxIncludeNotProcessed)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_5.addWidget(self.groupBox_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.retranslateUi(WebOrderWidget)

        QMetaObject.connectSlotsByName(WebOrderWidget)
    # setupUi

    def retranslateUi(self, WebOrderWidget):
        WebOrderWidget.setWindowTitle(QCoreApplication.translate("WebOrderWidget", u"Web orders", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("WebOrderWidget", u"Total order count", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("WebOrderWidget", u"Processed order count", None))
        self.groupBox.setTitle(QCoreApplication.translate("WebOrderWidget", u"Unprocessed order count", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("WebOrderWidget", u"Web order management", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("WebOrderWidget", u"Delete web orders", None))
        self.checkBoxIncludeNotProcessed.setText(QCoreApplication.translate("WebOrderWidget", u"Including orders not processed", None))
    # retranslateUi

