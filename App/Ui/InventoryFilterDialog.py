# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InventoryFilterDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_StockInventoryFilterDialog(object):
    def setupUi(self, StockInventoryFilterDialog):
        if not StockInventoryFilterDialog.objectName():
            StockInventoryFilterDialog.setObjectName(u"StockInventoryFilterDialog")
        StockInventoryFilterDialog.resize(240, 128)
        self.verticalLayout_3 = QVBoxLayout(StockInventoryFilterDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBoxEvent = QGroupBox(StockInventoryFilterDialog)
        self.groupBoxEvent.setObjectName(u"groupBoxEvent")
        self.verticalLayout = QVBoxLayout(self.groupBoxEvent)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBoxEvent = QComboBox(self.groupBoxEvent)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout.addWidget(self.comboBoxEvent)


        self.verticalLayout_2.addWidget(self.groupBoxEvent)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(StockInventoryFilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(StockInventoryFilterDialog)
        self.buttonBox.accepted.connect(StockInventoryFilterDialog.accept)
        self.buttonBox.rejected.connect(StockInventoryFilterDialog.reject)

        QMetaObject.connectSlotsByName(StockInventoryFilterDialog)
    # setupUi

    def retranslateUi(self, StockInventoryFilterDialog):
        StockInventoryFilterDialog.setWindowTitle(QCoreApplication.translate("StockInventoryFilterDialog", u"Dialog", None))
        self.groupBoxEvent.setTitle(QCoreApplication.translate("StockInventoryFilterDialog", u"Event", None))
    # retranslateUi

