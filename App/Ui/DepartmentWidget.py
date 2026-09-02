# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DepartmentWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QVBoxLayout,
    QWidget)

from App.Widget.View import EnhancedTableView

class Ui_DepartmentWidget(object):
    def setupUi(self, DepartmentWidget):
        if not DepartmentWidget.objectName():
            DepartmentWidget.setObjectName(u"DepartmentWidget")
        DepartmentWidget.resize(640, 480)
        self.verticalLayout = QVBoxLayout(DepartmentWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(DepartmentWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(DepartmentWidget)

        QMetaObject.connectSlotsByName(DepartmentWidget)
    # setupUi

    def retranslateUi(self, DepartmentWidget):
        DepartmentWidget.setWindowTitle(QCoreApplication.translate("DepartmentWidget", u"Department", None))
    # retranslateUi

