# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GenerateTableNumbersDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_GenerateTableNumbers(object):
    def setupUi(self, GenerateTableNumbers):
        if not GenerateTableNumbers.objectName():
            GenerateTableNumbers.setObjectName(u"GenerateTableNumbers")
        GenerateTableNumbers.resize(438, 410)
        self.verticalLayout_7 = QVBoxLayout(GenerateTableNumbers)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_2 = QGroupBox(GenerateTableNumbers)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.spinBoxStartRow = QSpinBox(self.groupBox_2)
        self.spinBoxStartRow.setObjectName(u"spinBoxStartRow")
        self.spinBoxStartRow.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxStartRow.setMinimum(1)
        self.spinBoxStartRow.setMaximum(999)
        self.spinBoxStartRow.setValue(1)

        self.horizontalLayout.addWidget(self.spinBoxStartRow)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.spinBoxRows = QSpinBox(self.groupBox_2)
        self.spinBoxRows.setObjectName(u"spinBoxRows")
        self.spinBoxRows.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxRows.setMinimum(1)
        self.spinBoxRows.setMaximum(999)
        self.spinBoxRows.setValue(1)

        self.horizontalLayout.addWidget(self.spinBoxRows)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout.addWidget(self.label_8)

        self.spinBoxColumns = QSpinBox(self.groupBox_2)
        self.spinBoxColumns.setObjectName(u"spinBoxColumns")
        self.spinBoxColumns.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxColumns.setMinimum(1)
        self.spinBoxColumns.setMaximum(999)
        self.spinBoxColumns.setValue(1)

        self.horizontalLayout.addWidget(self.spinBoxColumns)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.groupBox = QGroupBox(GenerateTableNumbers)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radioButtonRowColumn = QRadioButton(self.groupBox)
        self.radioButtonRowColumn.setObjectName(u"radioButtonRowColumn")
        self.radioButtonRowColumn.setChecked(True)

        self.verticalLayout_2.addWidget(self.radioButtonRowColumn)

        self.radioButtonColumnRow = QRadioButton(self.groupBox)
        self.radioButtonColumnRow.setObjectName(u"radioButtonColumnRow")

        self.verticalLayout_2.addWidget(self.radioButtonColumnRow)


        self.horizontalLayout_6.addLayout(self.verticalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 3, 1, 1)

        self.lineEditPrefix = QLineEdit(self.groupBox)
        self.lineEditPrefix.setObjectName(u"lineEditPrefix")
        self.lineEditPrefix.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lineEditPrefix, 1, 0, 1, 1)

        self.spinBoxRowPadding = QSpinBox(self.groupBox)
        self.spinBoxRowPadding.setObjectName(u"spinBoxRowPadding")
        self.spinBoxRowPadding.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxRowPadding.setMaximum(15)

        self.gridLayout.addWidget(self.spinBoxRowPadding, 1, 1, 1, 1)

        self.spinBoxColumnPadding = QSpinBox(self.groupBox)
        self.spinBoxColumnPadding.setObjectName(u"spinBoxColumnPadding")
        self.spinBoxColumnPadding.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBoxColumnPadding.setMaximum(99999)

        self.gridLayout.addWidget(self.spinBoxColumnPadding, 1, 2, 1, 1)

        self.lineEditSuffix = QLineEdit(self.groupBox)
        self.lineEditSuffix.setObjectName(u"lineEditSuffix")

        self.gridLayout.addWidget(self.lineEditSuffix, 1, 3, 1, 1)


        self.horizontalLayout_6.addLayout(self.gridLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(GenerateTableNumbers)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonChooseBackground = QPushButton(self.groupBox_3)
        self.pushButtonChooseBackground.setObjectName(u"pushButtonChooseBackground")

        self.horizontalLayout_4.addWidget(self.pushButtonChooseBackground)

        self.pushButtonExample = QPushButton(self.groupBox_3)
        self.pushButtonExample.setObjectName(u"pushButtonExample")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonExample.sizePolicy().hasHeightForWidth())
        self.pushButtonExample.setSizePolicy(sizePolicy)
        self.pushButtonExample.setMinimumSize(QSize(0, 40))
        self.pushButtonExample.setBaseSize(QSize(0, 0))

        self.horizontalLayout_4.addWidget(self.pushButtonExample)

        self.pushButtonChooseText = QPushButton(self.groupBox_3)
        self.pushButtonChooseText.setObjectName(u"pushButtonChooseText")

        self.horizontalLayout_4.addWidget(self.pushButtonChooseText)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(GenerateTableNumbers)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBoxChangeBackgroundColor = QCheckBox(self.groupBox_4)
        self.checkBoxChangeBackgroundColor.setObjectName(u"checkBoxChangeBackgroundColor")

        self.verticalLayout_4.addWidget(self.checkBoxChangeBackgroundColor)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pushButtonBGC4 = QPushButton(self.groupBox_4)
        self.pushButtonBGC4.setObjectName(u"pushButtonBGC4")
        self.pushButtonBGC4.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC4, 0, 3, 1, 1)

        self.pushButtonBGC5 = QPushButton(self.groupBox_4)
        self.pushButtonBGC5.setObjectName(u"pushButtonBGC5")
        self.pushButtonBGC5.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC5, 0, 4, 1, 1)

        self.pushButtonBGC2 = QPushButton(self.groupBox_4)
        self.pushButtonBGC2.setObjectName(u"pushButtonBGC2")
        self.pushButtonBGC2.setCheckable(False)
        self.pushButtonBGC2.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC2, 0, 1, 1, 1)

        self.pushButtonBGC3 = QPushButton(self.groupBox_4)
        self.pushButtonBGC3.setObjectName(u"pushButtonBGC3")
        self.pushButtonBGC3.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC3, 0, 2, 1, 1)

        self.pushButtonBGC1 = QPushButton(self.groupBox_4)
        self.pushButtonBGC1.setObjectName(u"pushButtonBGC1")
        self.pushButtonBGC1.setEnabled(True)
        self.pushButtonBGC1.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC1, 0, 0, 1, 1)

        self.pushButtonBGC6 = QPushButton(self.groupBox_4)
        self.pushButtonBGC6.setObjectName(u"pushButtonBGC6")
        self.pushButtonBGC6.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC6, 1, 0, 1, 1)

        self.pushButtonBGC8 = QPushButton(self.groupBox_4)
        self.pushButtonBGC8.setObjectName(u"pushButtonBGC8")
        self.pushButtonBGC8.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC8, 1, 2, 1, 1)

        self.pushButtonBGC7 = QPushButton(self.groupBox_4)
        self.pushButtonBGC7.setObjectName(u"pushButtonBGC7")
        self.pushButtonBGC7.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC7, 1, 1, 1, 1)

        self.pushButtonBGC9 = QPushButton(self.groupBox_4)
        self.pushButtonBGC9.setObjectName(u"pushButtonBGC9")
        self.pushButtonBGC9.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC9, 1, 3, 1, 1)

        self.pushButtonBGC10 = QPushButton(self.groupBox_4)
        self.pushButtonBGC10.setObjectName(u"pushButtonBGC10")
        self.pushButtonBGC10.setFlat(False)

        self.gridLayout_2.addWidget(self.pushButtonBGC10, 1, 4, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(418, 13, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonAddTables = QPushButton(GenerateTableNumbers)
        self.pushButtonAddTables.setObjectName(u"pushButtonAddTables")

        self.horizontalLayout_5.addWidget(self.pushButtonAddTables)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(GenerateTableNumbers)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.horizontalLayout_5.addWidget(self.buttonBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.retranslateUi(GenerateTableNumbers)
        self.buttonBox.accepted.connect(GenerateTableNumbers.accept)
        self.buttonBox.rejected.connect(GenerateTableNumbers.reject)

        QMetaObject.connectSlotsByName(GenerateTableNumbers)
    # setupUi

    def retranslateUi(self, GenerateTableNumbers):
        GenerateTableNumbers.setWindowTitle(QCoreApplication.translate("GenerateTableNumbers", u"Generate table numbers", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GenerateTableNumbers", u"Table position and number", None))
        self.label_6.setText(QCoreApplication.translate("GenerateTableNumbers", u"Start row", None))
        self.label_7.setText(QCoreApplication.translate("GenerateTableNumbers", u"Rows", None))
        self.label_8.setText(QCoreApplication.translate("GenerateTableNumbers", u"Columns", None))
        self.groupBox.setTitle(QCoreApplication.translate("GenerateTableNumbers", u"Table code", None))
        self.radioButtonRowColumn.setText(QCoreApplication.translate("GenerateTableNumbers", u"row + column", None))
        self.radioButtonColumnRow.setText(QCoreApplication.translate("GenerateTableNumbers", u"column + row", None))
        self.label_4.setText(QCoreApplication.translate("GenerateTableNumbers", u"Pefix", None))
        self.label_3.setText(QCoreApplication.translate("GenerateTableNumbers", u"Row padding", None))
        self.label.setText(QCoreApplication.translate("GenerateTableNumbers", u"Column padding", None))
        self.label_5.setText(QCoreApplication.translate("GenerateTableNumbers", u"Suffix", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("GenerateTableNumbers", u"Button color", None))
        self.pushButtonChooseBackground.setText(QCoreApplication.translate("GenerateTableNumbers", u"Background color ...", None))
        self.pushButtonExample.setText(QCoreApplication.translate("GenerateTableNumbers", u"Example", None))
        self.pushButtonChooseText.setText(QCoreApplication.translate("GenerateTableNumbers", u"Text color ...", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("GenerateTableNumbers", u"Background button color", None))
        self.checkBoxChangeBackgroundColor.setText(QCoreApplication.translate("GenerateTableNumbers", u"Change background color on change row/column", None))
        self.pushButtonBGC4.setText("")
        self.pushButtonBGC5.setText("")
        self.pushButtonBGC2.setText("")
        self.pushButtonBGC3.setText("")
        self.pushButtonBGC1.setText("")
        self.pushButtonBGC6.setText("")
        self.pushButtonBGC8.setText("")
        self.pushButtonBGC7.setText("")
        self.pushButtonBGC9.setText("")
        self.pushButtonBGC10.setText("")
        self.pushButtonAddTables.setText(QCoreApplication.translate("GenerateTableNumbers", u"Add tables", None))
    # retranslateUi

