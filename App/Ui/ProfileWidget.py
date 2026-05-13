# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProfileWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
    QHeaderView, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_ProfileWidget(object):
    def setupUi(self, ProfileWidget):
        if not ProfileWidget.objectName():
            ProfileWidget.setObjectName(u"ProfileWidget")
        ProfileWidget.resize(872, 533)
        self.verticalLayout_8 = QVBoxLayout(ProfileWidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.stackedWidget = QStackedWidget(ProfileWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_6 = QVBoxLayout(self.page1)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditCode = QLineEdit(self.groupBox_3)
        self.lineEditCode.setObjectName(u"lineEditCode")
        self.lineEditCode.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.lineEditCode)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.checkBoxSystem = QCheckBox(self.page1)
        self.checkBoxSystem.setObjectName(u"checkBoxSystem")
        self.checkBoxSystem.setEnabled(True)
        self.checkBoxSystem.setCheckable(True)

        self.verticalLayout_5.addWidget(self.checkBoxSystem)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(self.page1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonFillActions = QPushButton(self.groupBox_2)
        self.pushButtonFillActions.setObjectName(u"pushButtonFillActions")

        self.horizontalLayout.addWidget(self.pushButtonFillActions)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.page1)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonRead = QPushButton(self.groupBox)
        self.pushButtonRead.setObjectName(u"pushButtonRead")

        self.verticalLayout.addWidget(self.pushButtonRead)

        self.pushButtonWrite = QPushButton(self.groupBox)
        self.pushButtonWrite.setObjectName(u"pushButtonWrite")

        self.verticalLayout.addWidget(self.pushButtonWrite)

        self.pushButtonExecute = QPushButton(self.groupBox)
        self.pushButtonExecute.setObjectName(u"pushButtonExecute")

        self.verticalLayout.addWidget(self.pushButtonExecute)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_5.addWidget(self.groupBox)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_4 = QGroupBox(self.page1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditDescription = QLineEdit(self.groupBox_4)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.horizontalLayout_3.addWidget(self.lineEditDescription)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.tableViewActions = EnhancedTableView(self.page1)
        self.tableViewActions.setObjectName(u"tableViewActions")

        self.verticalLayout_3.addWidget(self.tableViewActions)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButtonAdd = QPushButton(self.page1)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout_6.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.page1)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout_6.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_5)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_4 = QVBoxLayout(self.page2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableView = EnhancedTableView(self.page2)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_4.addWidget(self.tableView)

        self.stackedWidget.addWidget(self.page2)

        self.verticalLayout_7.addWidget(self.stackedWidget)

        self.groupBox_5 = QGroupBox(ProfileWidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonDuplicate = QPushButton(self.groupBox_5)
        self.pushButtonDuplicate.setObjectName(u"pushButtonDuplicate")

        self.horizontalLayout_4.addWidget(self.pushButtonDuplicate)

        self.horizontalSpacer = QSpacerItem(927, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.verticalLayout_7.addWidget(self.groupBox_5)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        QWidget.setTabOrder(self.lineEditCode, self.lineEditDescription)
        QWidget.setTabOrder(self.lineEditDescription, self.checkBoxSystem)
        QWidget.setTabOrder(self.checkBoxSystem, self.pushButtonFillActions)
        QWidget.setTabOrder(self.pushButtonFillActions, self.pushButtonRead)
        QWidget.setTabOrder(self.pushButtonRead, self.pushButtonWrite)
        QWidget.setTabOrder(self.pushButtonWrite, self.pushButtonExecute)
        QWidget.setTabOrder(self.pushButtonExecute, self.tableViewActions)
        QWidget.setTabOrder(self.tableViewActions, self.tableView)

        self.retranslateUi(ProfileWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ProfileWidget)
    # setupUi

    def retranslateUi(self, ProfileWidget):
        ProfileWidget.setWindowTitle(QCoreApplication.translate("ProfileWidget", u"Profile", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ProfileWidget", u"Code", None))
        self.checkBoxSystem.setText(QCoreApplication.translate("ProfileWidget", u"System profile", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ProfileWidget", u"Actions", None))
        self.pushButtonFillActions.setText(QCoreApplication.translate("ProfileWidget", u"Fill actions", None))
        self.groupBox.setTitle(QCoreApplication.translate("ProfileWidget", u"Set all actions to", None))
        self.pushButtonRead.setText(QCoreApplication.translate("ProfileWidget", u"Read", None))
        self.pushButtonWrite.setText(QCoreApplication.translate("ProfileWidget", u"Write", None))
        self.pushButtonExecute.setText(QCoreApplication.translate("ProfileWidget", u"Execute", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ProfileWidget", u"Description", None))
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("ProfileWidget", u"Profile management", None))
        self.pushButtonDuplicate.setText(QCoreApplication.translate("ProfileWidget", u"Duplicate", None))
    # retranslateUi

