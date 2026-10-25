# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderPrintSettingsWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from App.Widget.Control import HostNameLineEdit
from App.Widget.View import EnhancedTableView

class Ui_OrderPrintSettingsWidget(object):
    def setupUi(self, OrderPrintSettingsWidget):
        if not OrderPrintSettingsWidget.objectName():
            OrderPrintSettingsWidget.setObjectName(u"OrderPrintSettingsWidget")
        OrderPrintSettingsWidget.resize(640, 480)
        self.verticalLayout = QVBoxLayout(OrderPrintSettingsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(OrderPrintSettingsWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(OrderPrintSettingsWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBoxFromHostName = QComboBox(OrderPrintSettingsWidget)
        self.comboBoxFromHostName.setObjectName(u"comboBoxFromHostName")

        self.horizontalLayout.addWidget(self.comboBoxFromHostName)

        self.label_2 = QLabel(OrderPrintSettingsWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEditNewHostName = HostNameLineEdit(OrderPrintSettingsWidget)
        self.lineEditNewHostName.setObjectName(u"lineEditNewHostName")

        self.horizontalLayout.addWidget(self.lineEditNewHostName)

        self.pushButtonCopySettings = QPushButton(OrderPrintSettingsWidget)
        self.pushButtonCopySettings.setObjectName(u"pushButtonCopySettings")

        self.horizontalLayout.addWidget(self.pushButtonCopySettings)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(OrderPrintSettingsWidget)

        QMetaObject.connectSlotsByName(OrderPrintSettingsWidget)
    # setupUi

    def retranslateUi(self, OrderPrintSettingsWidget):
        OrderPrintSettingsWidget.setWindowTitle(QCoreApplication.translate("OrderPrintSettingsWidget", u"Generic Form View", None))
        self.label.setText(QCoreApplication.translate("OrderPrintSettingsWidget", u"Copy from", None))
        self.label_2.setText(QCoreApplication.translate("OrderPrintSettingsWidget", u"to", None))
        self.pushButtonCopySettings.setText(QCoreApplication.translate("OrderPrintSettingsWidget", u"Copy settings", None))
    # retranslateUi

