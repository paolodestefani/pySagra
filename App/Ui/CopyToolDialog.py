# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CopyToolDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CopyToolDialog(object):
    def setupUi(self, CopyToolDialog):
        if not CopyToolDialog.objectName():
            CopyToolDialog.setObjectName(u"CopyToolDialog")
        CopyToolDialog.resize(512, 384)
        self.verticalLayout_6 = QVBoxLayout(CopyToolDialog)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.labelIcon = QLabel(CopyToolDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_5.addWidget(self.labelIcon)

        self.verticalSpacer = QSpacerItem(20, 29, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBoxUtility = QGroupBox(CopyToolDialog)
        self.groupBoxUtility.setObjectName(u"groupBoxUtility")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxUtility)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBoxCompany = QComboBox(self.groupBoxUtility)
        self.comboBoxCompany.setObjectName(u"comboBoxCompany")

        self.verticalLayout_3.addWidget(self.comboBoxCompany)


        self.verticalLayout_4.addWidget(self.groupBoxUtility)

        self.groupBoxWarning = QGroupBox(CopyToolDialog)
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


        self.verticalLayout_4.addWidget(self.groupBoxWarning)

        self.groupBoxDelete = QGroupBox(CopyToolDialog)
        self.groupBoxDelete.setObjectName(u"groupBoxDelete")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxDelete)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxItem = QCheckBox(self.groupBoxDelete)
        self.checkBoxItem.setObjectName(u"checkBoxItem")

        self.gridLayout.addWidget(self.checkBoxItem, 1, 1, 1, 1)

        self.checkBoxInventory = QCheckBox(self.groupBoxDelete)
        self.checkBoxInventory.setObjectName(u"checkBoxInventory")

        self.gridLayout.addWidget(self.checkBoxInventory, 2, 1, 1, 1)

        self.checkBoxPriceList = QCheckBox(self.groupBoxDelete)
        self.checkBoxPriceList.setObjectName(u"checkBoxPriceList")

        self.gridLayout.addWidget(self.checkBoxPriceList, 3, 1, 1, 1)

        self.checkBoxDepartment = QCheckBox(self.groupBoxDelete)
        self.checkBoxDepartment.setObjectName(u"checkBoxDepartment")

        self.gridLayout.addWidget(self.checkBoxDepartment, 0, 1, 1, 1)

        self.checkBoxCashDesk = QCheckBox(self.groupBoxDelete)
        self.checkBoxCashDesk.setObjectName(u"checkBoxCashDesk")

        self.gridLayout.addWidget(self.checkBoxCashDesk, 0, 0, 1, 1)

        self.checkBoxPrinterClass = QCheckBox(self.groupBoxDelete)
        self.checkBoxPrinterClass.setObjectName(u"checkBoxPrinterClass")

        self.gridLayout.addWidget(self.checkBoxPrinterClass, 1, 0, 1, 1)

        self.checkBoxTable = QCheckBox(self.groupBoxDelete)
        self.checkBoxTable.setObjectName(u"checkBoxTable")

        self.gridLayout.addWidget(self.checkBoxTable, 2, 0, 1, 1)

        self.checkBoxSetting = QCheckBox(self.groupBoxDelete)
        self.checkBoxSetting.setObjectName(u"checkBoxSetting")

        self.gridLayout.addWidget(self.checkBoxSetting, 3, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_4.addWidget(self.groupBoxDelete)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.buttonBox = QDialogButtonBox(CopyToolDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_6.addWidget(self.buttonBox)


        self.retranslateUi(CopyToolDialog)
        self.buttonBox.accepted.connect(CopyToolDialog.accept)
        self.buttonBox.rejected.connect(CopyToolDialog.reject)

        QMetaObject.connectSlotsByName(CopyToolDialog)
    # setupUi

    def retranslateUi(self, CopyToolDialog):
        CopyToolDialog.setWindowTitle(QCoreApplication.translate("CopyToolDialog", u"Copy tool", None))
        self.labelIcon.setText(QCoreApplication.translate("CopyToolDialog", u"Icon", None))
        self.groupBoxUtility.setTitle(QCoreApplication.translate("CopyToolDialog", u"Copy from company", None))
        self.groupBoxWarning.setTitle(QCoreApplication.translate("CopyToolDialog", u"Warning", None))
        self.labelWarning.setText(QCoreApplication.translate("CopyToolDialog", u"Copy text", None))
        self.groupBoxDelete.setTitle(QCoreApplication.translate("CopyToolDialog", u"What to copy", None))
        self.checkBoxItem.setText(QCoreApplication.translate("CopyToolDialog", u"Items", None))
        self.checkBoxInventory.setText(QCoreApplication.translate("CopyToolDialog", u"Inventory", None))
        self.checkBoxPriceList.setText(QCoreApplication.translate("CopyToolDialog", u"Price lists", None))
        self.checkBoxDepartment.setText(QCoreApplication.translate("CopyToolDialog", u"Departments", None))
        self.checkBoxCashDesk.setText(QCoreApplication.translate("CopyToolDialog", u"Cash desks", None))
        self.checkBoxPrinterClass.setText(QCoreApplication.translate("CopyToolDialog", u"Printer classes", None))
        self.checkBoxTable.setText(QCoreApplication.translate("CopyToolDialog", u"Tables", None))
        self.checkBoxSetting.setText(QCoreApplication.translate("CopyToolDialog", u"Settings", None))
    # retranslateUi

