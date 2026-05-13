# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PriceListWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_PriceListWidget(object):
    def setupUi(self, PriceListWidget):
        if not PriceListWidget.objectName():
            PriceListWidget.setObjectName(u"PriceListWidget")
        PriceListWidget.resize(980, 699)
        self.verticalLayout_5 = QVBoxLayout(PriceListWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.stackedWidget = QStackedWidget(PriceListWidget)
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
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
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

        self.groupBoxPrices = QGroupBox(self.page1)
        self.groupBoxPrices.setObjectName(u"groupBoxPrices")
        self.groupBoxPrices.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxPrices)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.tableViewPrices = EnhancedTableView(self.groupBoxPrices)
        self.tableViewPrices.setObjectName(u"tableViewPrices")

        self.verticalLayout_2.addWidget(self.tableViewPrices)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonAdd = QPushButton(self.groupBoxPrices)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_5.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.groupBoxPrices)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_5.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.groupBoxPrices)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonDuplicate = QPushButton(self.page1)
        self.pushButtonDuplicate.setObjectName(u"pushButtonDuplicate")

        self.horizontalLayout.addWidget(self.pushButtonDuplicate)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_7 = QVBoxLayout(self.page2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_7.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout_5.addWidget(self.stackedWidget)

        QWidget.setTabOrder(self.lineEditDescription, self.tableViewPrices)
        QWidget.setTabOrder(self.tableViewPrices, self.tableView)

        self.retranslateUi(PriceListWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PriceListWidget)
    # setupUi

    def retranslateUi(self, PriceListWidget):
        PriceListWidget.setWindowTitle(QCoreApplication.translate("PriceListWidget", u"Price list", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("PriceListWidget", u"Price list description", None))
        self.groupBoxPrices.setTitle(QCoreApplication.translate("PriceListWidget", u"Price list prices", None))
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
        self.pushButtonDuplicate.setText(QCoreApplication.translate("PriceListWidget", u"Duplicate", None))
    # retranslateUi

