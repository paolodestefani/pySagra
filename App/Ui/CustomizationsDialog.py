# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CustomizationsDialog.ui'
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
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_CustomizationsDialog(object):
    def setupUi(self, CustomizationsDialog):
        if not CustomizationsDialog.objectName():
            CustomizationsDialog.setObjectName(u"CustomizationsDialog")
        CustomizationsDialog.resize(230, 176)
        self.verticalLayout_5 = QVBoxLayout(CustomizationsDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(CustomizationsDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButtonExport = QPushButton(CustomizationsDialog)
        self.pushButtonExport.setObjectName(u"pushButtonExport")
        self.pushButtonExport.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonExport)

        self.pushButtonImport = QPushButton(CustomizationsDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")
        self.pushButtonImport.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonImport)

        self.pushButtonClear = QPushButton(CustomizationsDialog)
        self.pushButtonClear.setObjectName(u"pushButtonClear")
        self.pushButtonClear.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonClear)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(CustomizationsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_5.addWidget(self.buttonBox)


        self.retranslateUi(CustomizationsDialog)
        self.buttonBox.accepted.connect(CustomizationsDialog.accept)
        self.buttonBox.rejected.connect(CustomizationsDialog.reject)

        QMetaObject.connectSlotsByName(CustomizationsDialog)
    # setupUi

    def retranslateUi(self, CustomizationsDialog):
        CustomizationsDialog.setWindowTitle(QCoreApplication.translate("CustomizationsDialog", u"Dialog", None))
        self.labelIcon.setText(QCoreApplication.translate("CustomizationsDialog", u"Icon", None))
        self.pushButtonExport.setText(QCoreApplication.translate("CustomizationsDialog", u"Export", None))
        self.pushButtonImport.setText(QCoreApplication.translate("CustomizationsDialog", u"Import", None))
        self.pushButtonClear.setText(QCoreApplication.translate("CustomizationsDialog", u"Clear", None))
    # retranslateUi

