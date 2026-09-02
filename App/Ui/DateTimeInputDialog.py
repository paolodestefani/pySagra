# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DateTimeInputDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QDateTimeEdit,
    QDialog, QDialogButtonBox, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DateTimeInputDialog(object):
    def setupUi(self, DateTimeInputDialog):
        if not DateTimeInputDialog.objectName():
            DateTimeInputDialog.setObjectName(u"DateTimeInputDialog")
        DateTimeInputDialog.resize(256, 160)
        self.verticalLayout_2 = QVBoxLayout(DateTimeInputDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelText = QLabel(DateTimeInputDialog)
        self.labelText.setObjectName(u"labelText")

        self.verticalLayout.addWidget(self.labelText)

        self.dateTimeEdit = QDateTimeEdit(DateTimeInputDialog)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.dateTimeEdit.setMinimumDate(QDate(2000, 1, 1))
        self.dateTimeEdit.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.dateTimeEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(DateTimeInputDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(DateTimeInputDialog)
        self.buttonBox.accepted.connect(DateTimeInputDialog.accept)
        self.buttonBox.rejected.connect(DateTimeInputDialog.reject)

        QMetaObject.connectSlotsByName(DateTimeInputDialog)
    # setupUi

    def retranslateUi(self, DateTimeInputDialog):
        DateTimeInputDialog.setWindowTitle(QCoreApplication.translate("DateTimeInputDialog", u"DateInputDialog", None))
        self.labelText.setText(QCoreApplication.translate("DateTimeInputDialog", u"Text", None))
    # retranslateUi

