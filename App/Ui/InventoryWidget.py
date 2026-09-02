# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InventoryWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_InventoryWidget(object):
    def setupUi(self, InventoryWidget):
        if not InventoryWidget.objectName():
            InventoryWidget.setObjectName(u"InventoryWidget")
        InventoryWidget.resize(643, 388)
        self.verticalLayout = QVBoxLayout(InventoryWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(InventoryWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayoutNormal = QVBoxLayout(self.layoutWidget)
        self.verticalLayoutNormal.setObjectName(u"verticalLayoutNormal")
        self.verticalLayoutNormal.setContentsMargins(0, 0, 0, 0)
        self.labelNormalItem = QLabel(self.layoutWidget)
        self.labelNormalItem.setObjectName(u"labelNormalItem")
        font = QFont()
        font.setBold(True)
        self.labelNormalItem.setFont(font)
        self.labelNormalItem.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayoutNormal.addWidget(self.labelNormalItem)

        self.tableViewItem = EnhancedTableView(self.layoutWidget)
        self.tableViewItem.setObjectName(u"tableViewItem")

        self.verticalLayoutNormal.addWidget(self.tableViewItem)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutKit = QVBoxLayout()
        self.verticalLayoutKit.setObjectName(u"verticalLayoutKit")
        self.labelKit = QLabel(self.layoutWidget1)
        self.labelKit.setObjectName(u"labelKit")
        self.labelKit.setFont(font)
        self.labelKit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayoutKit.addWidget(self.labelKit)

        self.tableViewKit = EnhancedTableView(self.layoutWidget1)
        self.tableViewKit.setObjectName(u"tableViewKit")

        self.verticalLayoutKit.addWidget(self.tableViewKit)


        self.horizontalLayout.addLayout(self.verticalLayoutKit)

        self.verticalLayoutMenu = QVBoxLayout()
        self.verticalLayoutMenu.setObjectName(u"verticalLayoutMenu")
        self.labelMenu = QLabel(self.layoutWidget1)
        self.labelMenu.setObjectName(u"labelMenu")
        self.labelMenu.setFont(font)
        self.labelMenu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayoutMenu.addWidget(self.labelMenu)

        self.tableViewMenu = EnhancedTableView(self.layoutWidget1)
        self.tableViewMenu.setObjectName(u"tableViewMenu")

        self.verticalLayoutMenu.addWidget(self.tableViewMenu)


        self.horizontalLayout.addLayout(self.verticalLayoutMenu)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(InventoryWidget)

        QMetaObject.connectSlotsByName(InventoryWidget)
    # setupUi

    def retranslateUi(self, InventoryWidget):
        InventoryWidget.setWindowTitle(QCoreApplication.translate("InventoryWidget", u"Inventory", None))
        self.labelNormalItem.setText(QCoreApplication.translate("InventoryWidget", u"Normal items inventory", None))
        self.labelKit.setText(QCoreApplication.translate("InventoryWidget", u"Kit availability", None))
        self.labelMenu.setText(QCoreApplication.translate("InventoryWidget", u"Menu availability", None))
    # retranslateUi

