# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrintEmailDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox

class Ui_PrintEmailDialog(object):
    def setupUi(self, PrintEmailDialog):
        if not PrintEmailDialog.objectName():
            PrintEmailDialog.setObjectName(u"PrintEmailDialog")
        PrintEmailDialog.resize(800, 384)
        self.verticalLayout_3 = QVBoxLayout(PrintEmailDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollAreaEmail = QScrollArea(PrintEmailDialog)
        self.scrollAreaEmail.setObjectName(u"scrollAreaEmail")
        self.scrollAreaEmail.setWidgetResizable(True)
        self.scrollAreaWidgetContentsEmail = QWidget()
        self.scrollAreaWidgetContentsEmail.setObjectName(u"scrollAreaWidgetContentsEmail")
        self.scrollAreaWidgetContentsEmail.setGeometry(QRect(0, 0, 778, 333))
        self.verticalLayoutEmail = QVBoxLayout(self.scrollAreaWidgetContentsEmail)
        self.verticalLayoutEmail.setObjectName(u"verticalLayoutEmail")
        self.verticalLayoutEmail.setContentsMargins(6, 6, 6, 6)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)

        self.comboBoxSenderAccount = QComboBox(self.scrollAreaWidgetContentsEmail)
        self.comboBoxSenderAccount.setObjectName(u"comboBoxSenderAccount")

        self.gridLayout.addWidget(self.comboBoxSenderAccount, 0, 1, 1, 3)

        self.label_11 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.lineEditTo = QLineEdit(self.scrollAreaWidgetContentsEmail)
        self.lineEditTo.setObjectName(u"lineEditTo")

        self.gridLayout.addWidget(self.lineEditTo, 1, 1, 1, 3)

        self.label_12 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 2, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEditCc = QLineEdit(self.scrollAreaWidgetContentsEmail)
        self.lineEditCc.setObjectName(u"lineEditCc")

        self.horizontalLayout_6.addWidget(self.lineEditCc)

        self.label_13 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_6.addWidget(self.label_13)

        self.lineEditBcc = QLineEdit(self.scrollAreaWidgetContentsEmail)
        self.lineEditBcc.setObjectName(u"lineEditBcc")

        self.horizontalLayout_6.addWidget(self.lineEditBcc)


        self.gridLayout.addLayout(self.horizontalLayout_6, 2, 1, 1, 3)

        self.label_14 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 3, 0, 1, 1)

        self.lineEditSubject = QLineEdit(self.scrollAreaWidgetContentsEmail)
        self.lineEditSubject.setObjectName(u"lineEditSubject")

        self.gridLayout.addWidget(self.lineEditSubject, 3, 1, 1, 3)

        self.label_15 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout.addWidget(self.label_15, 4, 0, 1, 1)

        self.lineEditAttachment = QLineEdit(self.scrollAreaWidgetContentsEmail)
        self.lineEditAttachment.setObjectName(u"lineEditAttachment")

        self.gridLayout.addWidget(self.lineEditAttachment, 4, 1, 1, 1)

        self.label_16 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout.addWidget(self.label_16, 4, 2, 1, 1)

        self.checkBoxSenderCopy = QCheckBox(self.scrollAreaWidgetContentsEmail)
        self.checkBoxSenderCopy.setObjectName(u"checkBoxSenderCopy")

        self.gridLayout.addWidget(self.checkBoxSenderCopy, 4, 3, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxPrintCurrentPage = QCheckBox(self.scrollAreaWidgetContentsEmail)
        self.checkBoxPrintCurrentPage.setObjectName(u"checkBoxPrintCurrentPage")

        self.horizontalLayout.addWidget(self.checkBoxPrintCurrentPage)

        self.label_2 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBoxFromPage = QSpinBox(self.scrollAreaWidgetContentsEmail)
        self.spinBoxFromPage.setObjectName(u"spinBoxFromPage")
        self.spinBoxFromPage.setMinimum(1)
        self.spinBoxFromPage.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinBoxFromPage)

        self.label_3 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBoxToPage = QSpinBox(self.scrollAreaWidgetContentsEmail)
        self.spinBoxToPage.setObjectName(u"spinBoxToPage")
        self.spinBoxToPage.setMinimum(1)
        self.spinBoxToPage.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinBoxToPage)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_6 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.comboBoxPDFVersion = RelationalComboBox(self.scrollAreaWidgetContentsEmail)
        self.comboBoxPDFVersion.setObjectName(u"comboBoxPDFVersion")

        self.horizontalLayout.addWidget(self.comboBoxPDFVersion)

        self.label_7 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinBoxResolution = QSpinBox(self.scrollAreaWidgetContentsEmail)
        self.spinBoxResolution.setObjectName(u"spinBoxResolution")
        self.spinBoxResolution.setMinimum(20)
        self.spinBoxResolution.setMaximum(300)
        self.spinBoxResolution.setValue(96)

        self.horizontalLayout.addWidget(self.spinBoxResolution)

        self.label_8 = QLabel(self.scrollAreaWidgetContentsEmail)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout.addWidget(self.label_8)


        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 4)


        self.verticalLayoutEmail.addLayout(self.gridLayout)

        self.scrollAreaEmail.setWidget(self.scrollAreaWidgetContentsEmail)

        self.verticalLayout_2.addWidget(self.scrollAreaEmail)

        self.buttonBox = QDialogButtonBox(PrintEmailDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(PrintEmailDialog)
        self.buttonBox.accepted.connect(PrintEmailDialog.accept)
        self.buttonBox.rejected.connect(PrintEmailDialog.reject)
        self.checkBoxPrintCurrentPage.clicked["bool"].connect(self.spinBoxFromPage.setDisabled)
        self.checkBoxPrintCurrentPage.clicked["bool"].connect(self.spinBoxToPage.setDisabled)

        QMetaObject.connectSlotsByName(PrintEmailDialog)
    # setupUi

    def retranslateUi(self, PrintEmailDialog):
        PrintEmailDialog.setWindowTitle(QCoreApplication.translate("PrintEmailDialog", u"Dialog", None))
        self.label_10.setText(QCoreApplication.translate("PrintEmailDialog", u"Sender", None))
        self.label_11.setText(QCoreApplication.translate("PrintEmailDialog", u"To", None))
        self.label_12.setText(QCoreApplication.translate("PrintEmailDialog", u"Cc", None))
        self.label_13.setText(QCoreApplication.translate("PrintEmailDialog", u"Bcc", None))
        self.label_14.setText(QCoreApplication.translate("PrintEmailDialog", u"Subject", None))
        self.label_15.setText(QCoreApplication.translate("PrintEmailDialog", u"Attachment", None))
        self.label_16.setText(QCoreApplication.translate("PrintEmailDialog", u".pdf", None))
        self.checkBoxSenderCopy.setText(QCoreApplication.translate("PrintEmailDialog", u"Sender copy", None))
        self.checkBoxPrintCurrentPage.setText(QCoreApplication.translate("PrintEmailDialog", u"Print current page", None))
        self.label_2.setText(QCoreApplication.translate("PrintEmailDialog", u"From page n.", None))
        self.label_3.setText(QCoreApplication.translate("PrintEmailDialog", u"To page n.", None))
        self.label_6.setText(QCoreApplication.translate("PrintEmailDialog", u"PDF version", None))
        self.label_7.setText(QCoreApplication.translate("PrintEmailDialog", u"Resolution", None))
        self.label_8.setText(QCoreApplication.translate("PrintEmailDialog", u"dpi", None))
    # retranslateUi

