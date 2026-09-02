# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConnectionHistoryWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_ConnectionHistoryWidget(object):
    def setupUi(self, ConnectionHistoryWidget):
        if not ConnectionHistoryWidget.objectName():
            ConnectionHistoryWidget.setObjectName(u"ConnectionHistoryWidget")
        ConnectionHistoryWidget.resize(870, 465)
        self.verticalLayout_4 = QVBoxLayout(ConnectionHistoryWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableView = EnhancedTableView(ConnectionHistoryWidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setSortingEnabled(True)

        self.verticalLayout_3.addWidget(self.tableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_2 = QGroupBox(ConnectionHistoryWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonDeleteOlder = QPushButton(self.groupBox_2)
        self.pushButtonDeleteOlder.setObjectName(u"pushButtonDeleteOlder")

        self.horizontalLayout_2.addWidget(self.pushButtonDeleteOlder)

        self.pushButtonDeleteAll = QPushButton(self.groupBox_2)
        self.pushButtonDeleteAll.setObjectName(u"pushButtonDeleteAll")

        self.horizontalLayout_2.addWidget(self.pushButtonDeleteAll)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(ConnectionHistoryWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxAutomaticDeletion = QCheckBox(self.groupBox)
        self.checkBoxAutomaticDeletion.setObjectName(u"checkBoxAutomaticDeletion")

        self.horizontalLayout.addWidget(self.checkBoxAutomaticDeletion)

        self.spinBoxDays = QSpinBox(self.groupBox)
        self.spinBoxDays.setObjectName(u"spinBoxDays")
        self.spinBoxDays.setEnabled(False)
        self.spinBoxDays.setMaximum(2147483647)

        self.horizontalLayout.addWidget(self.spinBoxDays)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.pushButtonDeleteSetting = QPushButton(self.groupBox)
        self.pushButtonDeleteSetting.setObjectName(u"pushButtonDeleteSetting")

        self.horizontalLayout.addWidget(self.pushButtonDeleteSetting)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addWidget(self.groupBox)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.retranslateUi(ConnectionHistoryWidget)
        self.checkBoxAutomaticDeletion.clicked["bool"].connect(self.spinBoxDays.setEnabled)

        QMetaObject.connectSlotsByName(ConnectionHistoryWidget)
    # setupUi

    def retranslateUi(self, ConnectionHistoryWidget):
        ConnectionHistoryWidget.setWindowTitle(QCoreApplication.translate("ConnectionHistoryWidget", u"Connection history", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ConnectionHistoryWidget", u"Delete log records", None))
        self.pushButtonDeleteOlder.setText(QCoreApplication.translate("ConnectionHistoryWidget", u"Delete older records", None))
        self.pushButtonDeleteAll.setText(QCoreApplication.translate("ConnectionHistoryWidget", u"Delete all records", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConnectionHistoryWidget", u"Automatic log record deletion configuration", None))
        self.checkBoxAutomaticDeletion.setText(QCoreApplication.translate("ConnectionHistoryWidget", u"Automatic deletion after", None))
        self.label.setText(QCoreApplication.translate("ConnectionHistoryWidget", u"days", None))
        self.pushButtonDeleteSetting.setText(QCoreApplication.translate("ConnectionHistoryWidget", u"Update setting", None))
    # retranslateUi

