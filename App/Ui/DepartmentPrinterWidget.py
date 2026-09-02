# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DepartmentPrinterWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_DepartmentPrinterWidget(object):
    def setupUi(self, DepartmentPrinterWidget):
        if not DepartmentPrinterWidget.objectName():
            DepartmentPrinterWidget.setObjectName(u"DepartmentPrinterWidget")
        DepartmentPrinterWidget.resize(851, 450)
        self.verticalLayout_5 = QVBoxLayout(DepartmentPrinterWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(DepartmentPrinterWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_3 = QVBoxLayout(self.page1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEditDescription = QLineEdit(self.groupBox_3)
        self.lineEditDescription.setObjectName(u"lineEditDescription")
        self.lineEditDescription.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditDescription.sizePolicy().hasHeightForWidth())
        self.lineEditDescription.setSizePolicy(sizePolicy)
        self.lineEditDescription.setMinimumSize(QSize(150, 0))

        self.verticalLayout.addWidget(self.lineEditDescription)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBoxLocalPrinters = QGroupBox(self.page1)
        self.groupBoxLocalPrinters.setObjectName(u"groupBoxLocalPrinters")
        self.groupBoxLocalPrinters.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxLocalPrinters)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.printersTableView = EnhancedTableView(self.groupBoxLocalPrinters)
        self.printersTableView.setObjectName(u"printersTableView")

        self.verticalLayout_2.addWidget(self.printersTableView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonAdd = QPushButton(self.groupBoxLocalPrinters)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_5.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.groupBoxLocalPrinters)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_5.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.groupBoxLocalPrinters)

        self.stackedWidget.addWidget(self.page1)
        self.groupBoxLocalPrinters.raise_()
        self.groupBox_3.raise_()
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_7 = QVBoxLayout(self.page2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_7.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        QWidget.setTabOrder(self.lineEditDescription, self.printersTableView)
        QWidget.setTabOrder(self.printersTableView, self.tableView)

        self.retranslateUi(DepartmentPrinterWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DepartmentPrinterWidget)
    # setupUi

    def retranslateUi(self, DepartmentPrinterWidget):
        DepartmentPrinterWidget.setWindowTitle(QCoreApplication.translate("DepartmentPrinterWidget", u"Department Printer", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("DepartmentPrinterWidget", u"Printer class", None))
        self.groupBoxLocalPrinters.setTitle(QCoreApplication.translate("DepartmentPrinterWidget", u"Computer / printer association", None))
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
    # retranslateUi

