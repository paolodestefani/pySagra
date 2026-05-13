# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderProgressWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateEdit, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QSplitter, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_OrderProgressWidget(object):
    def setupUi(self, OrderProgressWidget):
        if not OrderProgressWidget.objectName():
            OrderProgressWidget.setObjectName(u"OrderProgressWidget")
        OrderProgressWidget.resize(777, 509)
        self.verticalLayout = QVBoxLayout(OrderProgressWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(OrderProgressWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout1Order = QVBoxLayout(self.layoutWidget)
        self.verticalLayout1Order.setObjectName(u"verticalLayout1Order")
        self.verticalLayout1Order.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout1Order.addWidget(self.label_4)

        self.tableViewOrder = EnhancedTableView(self.layoutWidget)
        self.tableViewOrder.setObjectName(u"tableViewOrder")

        self.verticalLayout1Order.addWidget(self.tableViewOrder)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.checkBoxAcquired = QCheckBox(self.layoutWidget)
        self.checkBoxAcquired.setObjectName(u"checkBoxAcquired")
        self.checkBoxAcquired.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout.addWidget(self.checkBoxAcquired)

        self.checkBoxInProgress = QCheckBox(self.layoutWidget)
        self.checkBoxInProgress.setObjectName(u"checkBoxInProgress")
        self.checkBoxInProgress.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout.addWidget(self.checkBoxInProgress)

        self.checkBoxProcessed = QCheckBox(self.layoutWidget)
        self.checkBoxProcessed.setObjectName(u"checkBoxProcessed")
        self.checkBoxProcessed.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout.addWidget(self.checkBoxProcessed)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBoxRecords = QSpinBox(self.layoutWidget)
        self.spinBoxRecords.setObjectName(u"spinBoxRecords")
        self.spinBoxRecords.setReadOnly(True)
        self.spinBoxRecords.setMaximum(9999)

        self.horizontalLayout.addWidget(self.spinBoxRecords)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.dateEdit = QDateEdit(self.layoutWidget)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.dateEdit)

        self.radioButtonLunch = QRadioButton(self.layoutWidget)
        self.radioButtonLunch.setObjectName(u"radioButtonLunch")

        self.horizontalLayout.addWidget(self.radioButtonLunch)

        self.radioButtonDinner = QRadioButton(self.layoutWidget)
        self.radioButtonDinner.setObjectName(u"radioButtonDinner")

        self.horizontalLayout.addWidget(self.radioButtonDinner)


        self.verticalLayout1Order.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout2Barcode = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout2Barcode.setObjectName(u"verticalLayout2Barcode")
        self.verticalLayout2Barcode.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout2Barcode.addWidget(self.label_2)

        self.tableWidgetScans = QTableWidget(self.layoutWidget_2)
        self.tableWidgetScans.setObjectName(u"tableWidgetScans")

        self.verticalLayout2Barcode.addWidget(self.tableWidgetScans)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.layoutWidget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditBarcode = QLineEdit(self.groupBox)
        self.lineEditBarcode.setObjectName(u"lineEditBarcode")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditBarcode.sizePolicy().hasHeightForWidth())
        self.lineEditBarcode.setSizePolicy(sizePolicy)
        self.lineEditBarcode.setMinimumSize(QSize(0, 0))
        self.lineEditBarcode.setStyleSheet(u"QLineEdit#lineEditBarcode {\n"
"	color: black;\n"
"	background: transparent;\n"
"	border: 3px solid blue;\n"
"	border-radius: 5px;\n"
"	padding: 0 8px;\n"
"}\n"
"QLineEdit#lineEditBarcode::focus {\n"
"	color: black;\n"
"	background: cyan;\n"
"	border: 3px solid blue;\n"
"	border-radius: 5px;\n"
"	padding: 0 8px;\n"
"}")
        self.lineEditBarcode.setClearButtonEnabled(False)

        self.verticalLayout_2.addWidget(self.lineEditBarcode)


        self.horizontalLayout_3.addWidget(self.groupBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.groupBox_2 = QGroupBox(self.layoutWidget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButtonSetAsUnprocessed = QPushButton(self.groupBox_2)
        self.pushButtonSetAsUnprocessed.setObjectName(u"pushButtonSetAsUnprocessed")

        self.verticalLayout_3.addWidget(self.pushButtonSetAsUnprocessed)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout2Barcode.addLayout(self.horizontalLayout_3)

        self.splitter.addWidget(self.layoutWidget_2)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(OrderProgressWidget)

        QMetaObject.connectSlotsByName(OrderProgressWidget)
    # setupUi

    def retranslateUi(self, OrderProgressWidget):
        OrderProgressWidget.setWindowTitle(QCoreApplication.translate("OrderProgressWidget", u"Order Progress", None))
        self.label_4.setText(QCoreApplication.translate("OrderProgressWidget", u"Order status", None))
        self.label.setText(QCoreApplication.translate("OrderProgressWidget", u"View orders", None))
        self.checkBoxAcquired.setText(QCoreApplication.translate("OrderProgressWidget", u"Acquired", None))
        self.checkBoxInProgress.setText(QCoreApplication.translate("OrderProgressWidget", u"In progress", None))
        self.checkBoxProcessed.setText(QCoreApplication.translate("OrderProgressWidget", u"Processed", None))
        self.label_3.setText(QCoreApplication.translate("OrderProgressWidget", u"Records:", None))
        self.label_5.setText(QCoreApplication.translate("OrderProgressWidget", u"Date:", None))
        self.radioButtonLunch.setText(QCoreApplication.translate("OrderProgressWidget", u"Lunch", None))
        self.radioButtonDinner.setText(QCoreApplication.translate("OrderProgressWidget", u"Dinner", None))
        self.label_2.setText(QCoreApplication.translate("OrderProgressWidget", u"Barcode scan", None))
        self.groupBox.setTitle(QCoreApplication.translate("OrderProgressWidget", u"Barcode scan", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OrderProgressWidget", u"Edit scan", None))
        self.pushButtonSetAsUnprocessed.setText(QCoreApplication.translate("OrderProgressWidget", u"Set as unprocessed", None))
    # retranslateUi

