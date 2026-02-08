# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrintPDFDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox

class Ui_PrintPDFDialog(object):
    def setupUi(self, PrintPDFDialog):
        if not PrintPDFDialog.objectName():
            PrintPDFDialog.setObjectName(u"PrintPDFDialog")
        PrintPDFDialog.setWindowModality(Qt.ApplicationModal)
        PrintPDFDialog.resize(480, 162)
        self.verticalLayout_2 = QVBoxLayout(PrintPDFDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(PrintPDFDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditDirectory = QLineEdit(PrintPDFDialog)
        self.lineEditDirectory.setObjectName(u"lineEditDirectory")

        self.gridLayout.addWidget(self.lineEditDirectory, 0, 1, 1, 1)

        self.pushButtonSelectDirectory = QPushButton(PrintPDFDialog)
        self.pushButtonSelectDirectory.setObjectName(u"pushButtonSelectDirectory")

        self.gridLayout.addWidget(self.pushButtonSelectDirectory, 0, 2, 1, 1)

        self.label_4 = QLabel(PrintPDFDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEditFileName = QLineEdit(PrintPDFDialog)
        self.lineEditFileName.setObjectName(u"lineEditFileName")

        self.gridLayout.addWidget(self.lineEditFileName, 1, 1, 1, 1)

        self.label_5 = QLabel(PrintPDFDialog)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBoxPrintCurrentPage = QCheckBox(PrintPDFDialog)
        self.checkBoxPrintCurrentPage.setObjectName(u"checkBoxPrintCurrentPage")

        self.horizontalLayout.addWidget(self.checkBoxPrintCurrentPage)

        self.label_2 = QLabel(PrintPDFDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spinBoxFromPage = QSpinBox(PrintPDFDialog)
        self.spinBoxFromPage.setObjectName(u"spinBoxFromPage")
        self.spinBoxFromPage.setEnabled(True)
        self.spinBoxFromPage.setMinimum(1)
        self.spinBoxFromPage.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinBoxFromPage)

        self.label_3 = QLabel(PrintPDFDialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.spinBoxToPage = QSpinBox(PrintPDFDialog)
        self.spinBoxToPage.setObjectName(u"spinBoxToPage")
        self.spinBoxToPage.setEnabled(True)
        self.spinBoxToPage.setMinimum(1)
        self.spinBoxToPage.setMaximum(999)

        self.horizontalLayout.addWidget(self.spinBoxToPage)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBoxOpenFile = QCheckBox(PrintPDFDialog)
        self.checkBoxOpenFile.setObjectName(u"checkBoxOpenFile")

        self.horizontalLayout_2.addWidget(self.checkBoxOpenFile)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_6 = QLabel(PrintPDFDialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.comboBoxPDFVersion = RelationalComboBox(PrintPDFDialog)
        self.comboBoxPDFVersion.setObjectName(u"comboBoxPDFVersion")

        self.horizontalLayout_2.addWidget(self.comboBoxPDFVersion)

        self.label_7 = QLabel(PrintPDFDialog)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.spinBoxResolution = QSpinBox(PrintPDFDialog)
        self.spinBoxResolution.setObjectName(u"spinBoxResolution")
        self.spinBoxResolution.setMinimum(20)
        self.spinBoxResolution.setMaximum(300)
        self.spinBoxResolution.setValue(96)

        self.horizontalLayout_2.addWidget(self.spinBoxResolution)

        self.label_8 = QLabel(PrintPDFDialog)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_2.addWidget(self.label_8)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(PrintPDFDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        QWidget.setTabOrder(self.pushButtonSelectDirectory, self.lineEditDirectory)
        QWidget.setTabOrder(self.lineEditDirectory, self.lineEditFileName)
        QWidget.setTabOrder(self.lineEditFileName, self.checkBoxPrintCurrentPage)
        QWidget.setTabOrder(self.checkBoxPrintCurrentPage, self.spinBoxFromPage)
        QWidget.setTabOrder(self.spinBoxFromPage, self.spinBoxToPage)
        QWidget.setTabOrder(self.spinBoxToPage, self.checkBoxOpenFile)
        QWidget.setTabOrder(self.checkBoxOpenFile, self.comboBoxPDFVersion)
        QWidget.setTabOrder(self.comboBoxPDFVersion, self.spinBoxResolution)

        self.retranslateUi(PrintPDFDialog)
        self.buttonBox.accepted.connect(PrintPDFDialog.accept)
        self.buttonBox.rejected.connect(PrintPDFDialog.reject)
        self.checkBoxPrintCurrentPage.clicked["bool"].connect(self.spinBoxFromPage.setDisabled)
        self.checkBoxPrintCurrentPage.clicked["bool"].connect(self.spinBoxToPage.setDisabled)

        QMetaObject.connectSlotsByName(PrintPDFDialog)
    # setupUi

    def retranslateUi(self, PrintPDFDialog):
        PrintPDFDialog.setWindowTitle(QCoreApplication.translate("PrintPDFDialog", u"Export to PDF file", None))
        self.label.setText(QCoreApplication.translate("PrintPDFDialog", u"Directory", None))
        self.pushButtonSelectDirectory.setText(QCoreApplication.translate("PrintPDFDialog", u"Select ...", None))
        self.label_4.setText(QCoreApplication.translate("PrintPDFDialog", u"File name", None))
        self.label_5.setText(QCoreApplication.translate("PrintPDFDialog", u".pdf", None))
        self.checkBoxPrintCurrentPage.setText(QCoreApplication.translate("PrintPDFDialog", u"Print current page", None))
        self.label_2.setText(QCoreApplication.translate("PrintPDFDialog", u"From page n.", None))
        self.label_3.setText(QCoreApplication.translate("PrintPDFDialog", u"To page n.", None))
        self.checkBoxOpenFile.setText(QCoreApplication.translate("PrintPDFDialog", u"Open file after creating it", None))
        self.label_6.setText(QCoreApplication.translate("PrintPDFDialog", u"PDF version", None))
        self.label_7.setText(QCoreApplication.translate("PrintPDFDialog", u"Resolution", None))
        self.label_8.setText(QCoreApplication.translate("PrintPDFDialog", u"dpi", None))
    # retranslateUi

