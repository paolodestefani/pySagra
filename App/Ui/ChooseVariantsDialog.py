# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChooseVariantsDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractSpinBox, QApplication, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ChooseVariantsDialog(object):
    def setupUi(self, ChooseVariantsDialog):
        if not ChooseVariantsDialog.objectName():
            ChooseVariantsDialog.setObjectName(u"ChooseVariantsDialog")
        ChooseVariantsDialog.resize(350, 200)
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

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditFreeVariant = QLineEdit(ChooseVariantsDialog)
        self.lineEditFreeVariant.setObjectName(u"lineEditFreeVariant")

        self.horizontalLayout.addWidget(self.lineEditFreeVariant)

        self.label = QLabel(ChooseVariantsDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.doubleSpinBoxPriceDelta = QDoubleSpinBox(ChooseVariantsDialog)
        self.doubleSpinBoxPriceDelta.setObjectName(u"doubleSpinBoxPriceDelta")
        self.doubleSpinBoxPriceDelta.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.doubleSpinBoxPriceDelta.setMaximum(999.000000000000000)

        self.horizontalLayout.addWidget(self.doubleSpinBoxPriceDelta)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(ChooseVariantsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        QWidget.setTabOrder(self.lineEditFreeVariant, self.doubleSpinBoxPriceDelta)
        QWidget.setTabOrder(self.doubleSpinBoxPriceDelta, self.buttonBox)

        self.retranslateUi(ChooseVariantsDialog)
        self.buttonBox.accepted.connect(ChooseVariantsDialog.accept)
        self.buttonBox.rejected.connect(ChooseVariantsDialog.reject)

        QMetaObject.connectSlotsByName(ChooseVariantsDialog)
    # setupUi

    def retranslateUi(self, ChooseVariantsDialog):
        ChooseVariantsDialog.setWindowTitle(QCoreApplication.translate("ChooseVariantsDialog", u"Varianti", None))
        self.label.setText(QCoreApplication.translate("ChooseVariantsDialog", u"+", None))
    # retranslateUi

