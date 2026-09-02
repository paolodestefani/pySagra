# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConnectionWidget.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from App.Widget.View import EnhancedTableView

class Ui_ConnectionWidget(object):
    def setupUi(self, ConnectionWidget):
        if not ConnectionWidget.objectName():
            ConnectionWidget.setObjectName(u"ConnectionWidget")
        ConnectionWidget.resize(678, 422)
        font = QFont()
        font.setKerning(True)
        ConnectionWidget.setFont(font)
        self.verticalLayout_4 = QVBoxLayout(ConnectionWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView = EnhancedTableView(ConnectionWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_3.addWidget(self.tableView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(ConnectionWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.killClientButton = QPushButton(self.groupBox)
        self.killClientButton.setObjectName(u"killClientButton")
        self.killClientButton.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.killClientButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.retranslateUi(ConnectionWidget)

        QMetaObject.connectSlotsByName(ConnectionWidget)
    # setupUi

    def retranslateUi(self, ConnectionWidget):
        ConnectionWidget.setWindowTitle(QCoreApplication.translate("ConnectionWidget", u"Connection", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConnectionWidget", u"Selected client", None))
        self.killClientButton.setText(QCoreApplication.translate("ConnectionWidget", u"Kill client", None))
    # retranslateUi

