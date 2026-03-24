# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChooseVariantsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ChooseVariantsDialog(object):
    def setupUi(self, ChooseVariantsDialog):
        if not ChooseVariantsDialog.objectName():
            ChooseVariantsDialog.setObjectName(u"ChooseVariantsDialog")
        ChooseVariantsDialog.resize(220, 170)
        ChooseVariantsDialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(ChooseVariantsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layout = QVBoxLayout()
        self.layout.setObjectName(u"layout")

        self.verticalLayout.addLayout(self.layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ChooseVariantsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ChooseVariantsDialog)
        self.buttonBox.accepted.connect(ChooseVariantsDialog.accept)
        self.buttonBox.rejected.connect(ChooseVariantsDialog.reject)

        QMetaObject.connectSlotsByName(ChooseVariantsDialog)
    # setupUi

    def retranslateUi(self, ChooseVariantsDialog):
        ChooseVariantsDialog.setWindowTitle(QCoreApplication.translate("ChooseVariantsDialog", u"Varianti", None))
    # retranslateUi

