# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IncomeSummaryFilterDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
    QDialogButtonBox, QGroupBox, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_IncomeSummaryFilterDialog(object):
    def setupUi(self, IncomeSummaryFilterDialog):
        if not IncomeSummaryFilterDialog.objectName():
            IncomeSummaryFilterDialog.setObjectName(u"IncomeSummaryFilterDialog")
        IncomeSummaryFilterDialog.resize(320, 200)
        self.verticalLayout_4 = QVBoxLayout(IncomeSummaryFilterDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(IncomeSummaryFilterDialog)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setBold(True)
        self.groupBox.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setBold(False)
        self.label.setFont(font1)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBoxEvent = QGroupBox(IncomeSummaryFilterDialog)
        self.groupBoxEvent.setObjectName(u"groupBoxEvent")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxEvent)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.comboBoxEvent = QComboBox(self.groupBoxEvent)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout_2.addWidget(self.comboBoxEvent)


        self.verticalLayout_3.addWidget(self.groupBoxEvent)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(IncomeSummaryFilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.retranslateUi(IncomeSummaryFilterDialog)
        self.buttonBox.accepted.connect(IncomeSummaryFilterDialog.accept)
        self.buttonBox.rejected.connect(IncomeSummaryFilterDialog.reject)

        QMetaObject.connectSlotsByName(IncomeSummaryFilterDialog)
    # setupUi

    def retranslateUi(self, IncomeSummaryFilterDialog):
        IncomeSummaryFilterDialog.setWindowTitle(QCoreApplication.translate("IncomeSummaryFilterDialog", u"Sales summary filter dialog", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("IncomeSummaryFilterDialog", u"Select the working event from the list below", None))
        self.groupBoxEvent.setTitle(QCoreApplication.translate("IncomeSummaryFilterDialog", u"Event", None))
    # retranslateUi

