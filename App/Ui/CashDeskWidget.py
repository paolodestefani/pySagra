# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CashDeskWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QVBoxLayout,
    QWidget)

from App.Widget.View import EnhancedTableView

class Ui_CashDeskWidget(object):
    def setupUi(self, CashDeskWidget):
        if not CashDeskWidget.objectName():
            CashDeskWidget.setObjectName(u"CashDeskWidget")
        CashDeskWidget.resize(640, 480)
        self.verticalLayout = QVBoxLayout(CashDeskWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(CashDeskWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(CashDeskWidget)

        QMetaObject.connectSlotsByName(CashDeskWidget)
    # setupUi

    def retranslateUi(self, CashDeskWidget):
        CashDeskWidget.setWindowTitle(QCoreApplication.translate("CashDeskWidget", u"Cash Desk", None))
    # retranslateUi

