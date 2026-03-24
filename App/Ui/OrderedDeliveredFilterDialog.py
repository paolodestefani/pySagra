# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OrderedDeliveredFilterDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateEdit,
    QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_StockUnloadFilterDialog(object):
    def setupUi(self, StockUnloadFilterDialog):
        if not StockUnloadFilterDialog.objectName():
            StockUnloadFilterDialog.setObjectName(u"StockUnloadFilterDialog")
        StockUnloadFilterDialog.resize(240, 240)
        self.verticalLayout_5 = QVBoxLayout(StockUnloadFilterDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBoxEvent = QGroupBox(StockUnloadFilterDialog)
        self.groupBoxEvent.setObjectName(u"groupBoxEvent")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxEvent)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.comboBoxEvent = QComboBox(self.groupBoxEvent)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout_2.addWidget(self.comboBoxEvent)


        self.verticalLayout_4.addWidget(self.groupBoxEvent)

        self.groupBoxDate = QGroupBox(StockUnloadFilterDialog)
        self.groupBoxDate.setObjectName(u"groupBoxDate")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxDate)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.dateEditDate = QDateEdit(self.groupBoxDate)
        self.dateEditDate.setObjectName(u"dateEditDate")
        self.dateEditDate.setCalendarPopup(True)

        self.verticalLayout_3.addWidget(self.dateEditDate)


        self.verticalLayout_4.addWidget(self.groupBoxDate)

        self.groupBoxDayPart = QGroupBox(StockUnloadFilterDialog)
        self.groupBoxDayPart.setObjectName(u"groupBoxDayPart")
        self.verticalLayout = QVBoxLayout(self.groupBoxDayPart)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButtonLunch = QRadioButton(self.groupBoxDayPart)
        self.radioButtonLunch.setObjectName(u"radioButtonLunch")
        self.radioButtonLunch.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButtonLunch)

        self.radioButtonDinner = QRadioButton(self.groupBoxDayPart)
        self.radioButtonDinner.setObjectName(u"radioButtonDinner")

        self.horizontalLayout_2.addWidget(self.radioButtonDinner)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addWidget(self.groupBoxDayPart)

        self.verticalSpacer = QSpacerItem(20, 17, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(StockUnloadFilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.retranslateUi(StockUnloadFilterDialog)
        self.buttonBox.accepted.connect(StockUnloadFilterDialog.accept)
        self.buttonBox.rejected.connect(StockUnloadFilterDialog.reject)

        QMetaObject.connectSlotsByName(StockUnloadFilterDialog)
    # setupUi

    def retranslateUi(self, StockUnloadFilterDialog):
        StockUnloadFilterDialog.setWindowTitle(QCoreApplication.translate("StockUnloadFilterDialog", u"Dialog", None))
        self.groupBoxEvent.setTitle(QCoreApplication.translate("StockUnloadFilterDialog", u"Event", None))
        self.groupBoxDate.setTitle(QCoreApplication.translate("StockUnloadFilterDialog", u"Date", None))
        self.groupBoxDayPart.setTitle(QCoreApplication.translate("StockUnloadFilterDialog", u"Day part", None))
        self.radioButtonLunch.setText(QCoreApplication.translate("StockUnloadFilterDialog", u"Lunch", None))
        self.radioButtonDinner.setText(QCoreApplication.translate("StockUnloadFilterDialog", u"Dinner", None))
    # retranslateUi

