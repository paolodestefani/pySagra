# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MenuWidget.ui'
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
    QSpacerItem, QStackedWidget, QTreeView, QVBoxLayout,
    QWidget)

from App.Widget.View import EnhancedTableView

class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        if not MenuWidget.objectName():
            MenuWidget.setObjectName(u"MenuWidget")
        MenuWidget.resize(764, 512)
        self.verticalLayout_7 = QVBoxLayout(MenuWidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.stackedWidget = QStackedWidget(MenuWidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_5 = QVBoxLayout(self.page1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditCode = QLineEdit(self.groupBox_3)
        self.lineEditCode.setObjectName(u"lineEditCode")
        self.lineEditCode.setEnabled(False)

        self.verticalLayout_2.addWidget(self.lineEditCode)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.checkBoxSystem = QCheckBox(self.page1)
        self.checkBoxSystem.setObjectName(u"checkBoxSystem")
        self.checkBoxSystem.setCheckable(True)

        self.verticalLayout_3.addWidget(self.checkBoxSystem)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_4 = QGroupBox(self.page1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEditDescription = QLineEdit(self.groupBox_4)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.horizontalLayout_3.addWidget(self.lineEditDescription)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.treeViewMenuItems = QTreeView(self.page1)
        self.treeViewMenuItems.setObjectName(u"treeViewMenuItems")

        self.verticalLayout.addWidget(self.treeViewMenuItems)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonAddChild = QPushButton(self.page1)
        self.pushButtonAddChild.setObjectName(u"pushButtonAddChild")

        self.horizontalLayout.addWidget(self.pushButtonAddChild)

        self.pushButtonAdd = QPushButton(self.page1)
        self.pushButtonAdd.setObjectName(u"pushButtonAdd")

        self.horizontalLayout.addWidget(self.pushButtonAdd)

        self.pushButtonRemove = QPushButton(self.page1)
        self.pushButtonRemove.setObjectName(u"pushButtonRemove")

        self.horizontalLayout.addWidget(self.pushButtonRemove)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

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

        QWidget.setTabOrder(self.lineEditCode, self.lineEditDescription)
        QWidget.setTabOrder(self.lineEditDescription, self.checkBoxSystem)
        QWidget.setTabOrder(self.checkBoxSystem, self.treeViewMenuItems)
        QWidget.setTabOrder(self.treeViewMenuItems, self.tableView)

        self.retranslateUi(MenuWidget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MenuWidget)
    # setupUi

    def retranslateUi(self, MenuWidget):
        MenuWidget.setWindowTitle(QCoreApplication.translate("MenuWidget", u"Menu", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MenuWidget", u"Code", None))
        self.checkBoxSystem.setText(QCoreApplication.translate("MenuWidget", u"System menu", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MenuWidget", u"Description", None))
        self.pushButtonAddChild.setText("")
        self.pushButtonAdd.setText("")
        self.pushButtonRemove.setText("")
    # retranslateUi

