# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChooseItemDialog.ui'
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
    QDialogButtonBox, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ChooseItemDialog(object):
    def setupUi(self, ChooseItemDialog):
        if not ChooseItemDialog.objectName():
            ChooseItemDialog.setObjectName(u"ChooseItemDialog")
        ChooseItemDialog.resize(240, 131)
        self.verticalLayout_2 = QVBoxLayout(ChooseItemDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ChooseItemDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.comboBoxItems = QComboBox(ChooseItemDialog)
        self.comboBoxItems.setObjectName(u"comboBoxItems")

        self.verticalLayout.addWidget(self.comboBoxItems)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ChooseItemDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ChooseItemDialog)
        self.buttonBox.accepted.connect(ChooseItemDialog.accept)
        self.buttonBox.rejected.connect(ChooseItemDialog.reject)

        QMetaObject.connectSlotsByName(ChooseItemDialog)
    # setupUi

    def retranslateUi(self, ChooseItemDialog):
        ChooseItemDialog.setWindowTitle(QCoreApplication.translate("ChooseItemDialog", u"Select", None))
        self.label.setText(QCoreApplication.translate("ChooseItemDialog", u"Select an item from the list below", None))
    # retranslateUi

