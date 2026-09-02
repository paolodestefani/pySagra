# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DeleteToolDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DeleteToolDialog(object):
    def setupUi(self, DeleteToolDialog):
        if not DeleteToolDialog.objectName():
            DeleteToolDialog.setObjectName(u"DeleteToolDialog")
        DeleteToolDialog.resize(432, 356)
        self.verticalLayout_5 = QVBoxLayout(DeleteToolDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.labelIcon = QLabel(DeleteToolDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_4.addWidget(self.labelIcon)

        self.verticalSpacer = QSpacerItem(20, 29, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBoxWarning = QGroupBox(DeleteToolDialog)
        self.groupBoxWarning.setObjectName(u"groupBoxWarning")
        font = QFont()
        font.setBold(True)
        self.groupBoxWarning.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBoxWarning)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelWarning = QLabel(self.groupBoxWarning)
        self.labelWarning.setObjectName(u"labelWarning")
        font1 = QFont()
        font1.setBold(False)
        self.labelWarning.setFont(font1)
        self.labelWarning.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelWarning)


        self.verticalLayout_3.addWidget(self.groupBoxWarning)

        self.groupBoxDelete = QGroupBox(DeleteToolDialog)
        self.groupBoxDelete.setObjectName(u"groupBoxDelete")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxDelete)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxOrder = QCheckBox(self.groupBoxDelete)
        self.checkBoxOrder.setObjectName(u"checkBoxOrder")

        self.gridLayout.addWidget(self.checkBoxOrder, 0, 0, 1, 1)

        self.checkBoxItem = QCheckBox(self.groupBoxDelete)
        self.checkBoxItem.setObjectName(u"checkBoxItem")

        self.gridLayout.addWidget(self.checkBoxItem, 0, 1, 1, 1)

        self.checkBoxTable = QCheckBox(self.groupBoxDelete)
        self.checkBoxTable.setObjectName(u"checkBoxTable")

        self.gridLayout.addWidget(self.checkBoxTable, 2, 1, 1, 1)

        self.checkBoxCashDesk = QCheckBox(self.groupBoxDelete)
        self.checkBoxCashDesk.setObjectName(u"checkBoxCashDesk")

        self.gridLayout.addWidget(self.checkBoxCashDesk, 3, 1, 1, 1)

        self.checkBoxPrinterClass = QCheckBox(self.groupBoxDelete)
        self.checkBoxPrinterClass.setObjectName(u"checkBoxPrinterClass")

        self.gridLayout.addWidget(self.checkBoxPrinterClass, 4, 1, 1, 1)

        self.checkBoxInventory = QCheckBox(self.groupBoxDelete)
        self.checkBoxInventory.setObjectName(u"checkBoxInventory")

        self.gridLayout.addWidget(self.checkBoxInventory, 1, 0, 1, 1)

        self.checkBoxEvent = QCheckBox(self.groupBoxDelete)
        self.checkBoxEvent.setObjectName(u"checkBoxEvent")

        self.gridLayout.addWidget(self.checkBoxEvent, 4, 0, 1, 1)

        self.checkBoxDepartment = QCheckBox(self.groupBoxDelete)
        self.checkBoxDepartment.setObjectName(u"checkBoxDepartment")

        self.gridLayout.addWidget(self.checkBoxDepartment, 1, 1, 1, 1)

        self.checkBoxPriceList = QCheckBox(self.groupBoxDelete)
        self.checkBoxPriceList.setObjectName(u"checkBoxPriceList")

        self.gridLayout.addWidget(self.checkBoxPriceList, 3, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_3.addWidget(self.groupBoxDelete)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 84, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(DeleteToolDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_5.addWidget(self.buttonBox)


        self.retranslateUi(DeleteToolDialog)
        self.buttonBox.accepted.connect(DeleteToolDialog.accept)
        self.buttonBox.rejected.connect(DeleteToolDialog.reject)

        QMetaObject.connectSlotsByName(DeleteToolDialog)
    # setupUi

    def retranslateUi(self, DeleteToolDialog):
        DeleteToolDialog.setWindowTitle(QCoreApplication.translate("DeleteToolDialog", u"Delete tool", None))
        self.labelIcon.setText(QCoreApplication.translate("DeleteToolDialog", u"Icon", None))
        self.groupBoxWarning.setTitle(QCoreApplication.translate("DeleteToolDialog", u"Warning", None))
        self.labelWarning.setText(QCoreApplication.translate("DeleteToolDialog", u"Delete text", None))
        self.groupBoxDelete.setTitle(QCoreApplication.translate("DeleteToolDialog", u"What to delete", None))
        self.checkBoxOrder.setText(QCoreApplication.translate("DeleteToolDialog", u"Orders", None))
        self.checkBoxItem.setText(QCoreApplication.translate("DeleteToolDialog", u"Items", None))
        self.checkBoxTable.setText(QCoreApplication.translate("DeleteToolDialog", u"Tables", None))
        self.checkBoxCashDesk.setText(QCoreApplication.translate("DeleteToolDialog", u"Cash desks", None))
        self.checkBoxPrinterClass.setText(QCoreApplication.translate("DeleteToolDialog", u"Printer classes", None))
        self.checkBoxInventory.setText(QCoreApplication.translate("DeleteToolDialog", u"Inventory", None))
        self.checkBoxEvent.setText(QCoreApplication.translate("DeleteToolDialog", u"Events", None))
        self.checkBoxDepartment.setText(QCoreApplication.translate("DeleteToolDialog", u"Departments", None))
        self.checkBoxPriceList.setText(QCoreApplication.translate("DeleteToolDialog", u"Price lists", None))
    # retranslateUi

