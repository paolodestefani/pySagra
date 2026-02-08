# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderProgressWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox
from App.Widget.View import EnhancedTableView

class Ui_OrderProgressWidget(object):
    def setupUi(self, OrderProgressWidget):
        if not OrderProgressWidget.objectName():
            OrderProgressWidget.setObjectName(u"OrderProgressWidget")
        OrderProgressWidget.resize(667, 459)
        OrderProgressWidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.verticalLayout_5 = QVBoxLayout(OrderProgressWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter = QSplitter(OrderProgressWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4)

        self.tableViewOrder = EnhancedTableView(self.layoutWidget)
        self.tableViewOrder.setObjectName(u"tableViewOrder")

        self.verticalLayout_4.addWidget(self.tableViewOrder)

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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.comboBoxLimit = RelationalComboBox(self.layoutWidget)
        self.comboBoxLimit.setObjectName(u"comboBoxLimit")
        self.comboBoxLimit.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.horizontalLayout.addWidget(self.comboBoxLimit)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.tableWidgetScans = QTableWidget(self.layoutWidget1)
        self.tableWidgetScans.setObjectName(u"tableWidgetScans")

        self.verticalLayout.addWidget(self.tableWidgetScans)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox = QGroupBox(self.layoutWidget1)
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

        self.groupBox_2 = QGroupBox(self.layoutWidget1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButtonSetAsUnprocessed = QPushButton(self.groupBox_2)
        self.pushButtonSetAsUnprocessed.setObjectName(u"pushButtonSetAsUnprocessed")

        self.verticalLayout_3.addWidget(self.pushButtonSetAsUnprocessed)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_5.addWidget(self.splitter)

        QWidget.setTabOrder(self.tableViewOrder, self.checkBoxAcquired)
        QWidget.setTabOrder(self.checkBoxAcquired, self.checkBoxInProgress)
        QWidget.setTabOrder(self.checkBoxInProgress, self.checkBoxProcessed)
        QWidget.setTabOrder(self.checkBoxProcessed, self.comboBoxLimit)
        QWidget.setTabOrder(self.comboBoxLimit, self.tableWidgetScans)
        QWidget.setTabOrder(self.tableWidgetScans, self.lineEditBarcode)
        QWidget.setTabOrder(self.lineEditBarcode, self.pushButtonSetAsUnprocessed)

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
        self.label_3.setText(QCoreApplication.translate("OrderProgressWidget", u"Limit to", None))
        self.label_2.setText(QCoreApplication.translate("OrderProgressWidget", u"Barcode scan", None))
        self.groupBox.setTitle(QCoreApplication.translate("OrderProgressWidget", u"Barcode scan", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("OrderProgressWidget", u"Edit scan", None))
        self.pushButtonSetAsUnprocessed.setText(QCoreApplication.translate("OrderProgressWidget", u"Set as unprocessed", None))
    # retranslateUi

