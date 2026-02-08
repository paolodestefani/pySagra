# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SalesSummaryWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHeaderView, QSizePolicy,
    QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_SalesSummaryWidget(object):
    def setupUi(self, SalesSummaryWidget):
        if not SalesSummaryWidget.objectName():
            SalesSummaryWidget.setObjectName(u"SalesSummaryWidget")
        SalesSummaryWidget.resize(640, 480)
        self.verticalLayout = QVBoxLayout(SalesSummaryWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(SalesSummaryWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.checkBoxDetail = QCheckBox(SalesSummaryWidget)
        self.checkBoxDetail.setObjectName(u"checkBoxDetail")
        self.checkBoxDetail.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.verticalLayout.addWidget(self.checkBoxDetail)


        self.retranslateUi(SalesSummaryWidget)

        QMetaObject.connectSlotsByName(SalesSummaryWidget)
    # setupUi

    def retranslateUi(self, SalesSummaryWidget):
        SalesSummaryWidget.setWindowTitle(QCoreApplication.translate("SalesSummaryWidget", u"Sales summary", None))
        self.checkBoxDetail.setText(QCoreApplication.translate("SalesSummaryWidget", u"Show daily detail", None))
    # retranslateUi

