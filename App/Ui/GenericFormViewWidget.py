# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GenericFormViewWidget.ui'
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

class Ui_GenericFormViewWidget(object):
    def setupUi(self, GenericFormViewWidget):
        if not GenericFormViewWidget.objectName():
            GenericFormViewWidget.setObjectName(u"GenericFormViewWidget")
        GenericFormViewWidget.resize(640, 480)
        self.verticalLayout = QVBoxLayout(GenericFormViewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(GenericFormViewWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(GenericFormViewWidget)

        QMetaObject.connectSlotsByName(GenericFormViewWidget)
    # setupUi

    def retranslateUi(self, GenericFormViewWidget):
        GenericFormViewWidget.setWindowTitle(QCoreApplication.translate("GenericFormViewWidget", u"Generic Form View", None))
    # retranslateUi

