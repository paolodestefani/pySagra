# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderedDeliveredWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateTimeEdit, QHBoxLayout,
    QHeaderView, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_OrderedDeliveredWidget(object):
    def setupUi(self, OrderedDeliveredWidget):
        if not OrderedDeliveredWidget.objectName():
            OrderedDeliveredWidget.setObjectName(u"OrderedDeliveredWidget")
        OrderedDeliveredWidget.resize(679, 471)
        self.verticalLayout_2 = QVBoxLayout(OrderedDeliveredWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = EnhancedTableView(OrderedDeliveredWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxOnlyOrdered = QCheckBox(OrderedDeliveredWidget)
        self.checkBoxOnlyOrdered.setObjectName(u"checkBoxOnlyOrdered")

        self.horizontalLayout.addWidget(self.checkBoxOnlyOrdered)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.checkBoxAutomaticUpdate = QCheckBox(OrderedDeliveredWidget)
        self.checkBoxAutomaticUpdate.setObjectName(u"checkBoxAutomaticUpdate")

        self.horizontalLayout.addWidget(self.checkBoxAutomaticUpdate)

        self.label = QLabel(OrderedDeliveredWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.dateTimeEdit = QDateTimeEdit(OrderedDeliveredWidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setEnabled(False)
        self.dateTimeEdit.setReadOnly(True)
        self.dateTimeEdit.setCurrentSectionIndex(0)

        self.horizontalLayout.addWidget(self.dateTimeEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(OrderedDeliveredWidget)
        self.checkBoxAutomaticUpdate.clicked["bool"].connect(self.dateTimeEdit.setEnabled)

        QMetaObject.connectSlotsByName(OrderedDeliveredWidget)
    # setupUi

    def retranslateUi(self, OrderedDeliveredWidget):
        OrderedDeliveredWidget.setWindowTitle(QCoreApplication.translate("OrderedDeliveredWidget", u"Ordered delivered", None))
        self.checkBoxOnlyOrdered.setText(QCoreApplication.translate("OrderedDeliveredWidget", u"Only Ordered", None))
        self.checkBoxAutomaticUpdate.setText(QCoreApplication.translate("OrderedDeliveredWidget", u"Automatic update", None))
        self.label.setText(QCoreApplication.translate("OrderedDeliveredWidget", u"Last update:", None))
        self.dateTimeEdit.setDisplayFormat(QCoreApplication.translate("OrderedDeliveredWidget", u"MM/dd/yyyy HH:mm", None))
    # retranslateUi

