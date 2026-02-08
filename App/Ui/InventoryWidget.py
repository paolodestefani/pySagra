# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InventoryWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_InventoryWidget(object):
    def setupUi(self, InventoryWidget):
        if not InventoryWidget.objectName():
            InventoryWidget.setObjectName(u"InventoryWidget")
        InventoryWidget.resize(640, 413)
        self.verticalLayout_4 = QVBoxLayout(InventoryWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter = QSplitter(InventoryWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.setOpaqueResize(True)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)

        self.tableViewItem = EnhancedTableView(self.layoutWidget)
        self.tableViewItem.setObjectName(u"tableViewItem")

        self.verticalLayout_3.addWidget(self.tableViewItem)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.tableViewKit = EnhancedTableView(self.layoutWidget1)
        self.tableViewKit.setObjectName(u"tableViewKit")

        self.verticalLayout.addWidget(self.tableViewKit)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.tableViewMenu = EnhancedTableView(self.layoutWidget1)
        self.tableViewMenu.setObjectName(u"tableViewMenu")

        self.verticalLayout_2.addWidget(self.tableViewMenu)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_4.addWidget(self.splitter)


        self.retranslateUi(InventoryWidget)

        QMetaObject.connectSlotsByName(InventoryWidget)
    # setupUi

    def retranslateUi(self, InventoryWidget):
        InventoryWidget.setWindowTitle(QCoreApplication.translate("InventoryWidget", u"Inventory", None))
        self.label_4.setText(QCoreApplication.translate("InventoryWidget", u"Normal items inventory", None))
        self.label.setText(QCoreApplication.translate("InventoryWidget", u"Kit availability", None))
        self.label_2.setText(QCoreApplication.translate("InventoryWidget", u"Menu availability", None))
    # retranslateUi

