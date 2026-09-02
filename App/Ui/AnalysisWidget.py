# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AnalysisWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from App.Widget.View import EnhancedTableView

class Ui_AnalysisWidget(object):
    def setupUi(self, AnalysisWidget):
        if not AnalysisWidget.objectName():
            AnalysisWidget.setObjectName(u"AnalysisWidget")
        AnalysisWidget.resize(765, 517)
        self.verticalLayout_6 = QVBoxLayout(AnalysisWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBoxValues = QGroupBox(AnalysisWidget)
        self.groupBoxValues.setObjectName(u"groupBoxValues")
        self.verticalLayout = QVBoxLayout(self.groupBoxValues)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBoxFunction1 = QComboBox(self.groupBoxValues)
        self.comboBoxFunction1.setObjectName(u"comboBoxFunction1")

        self.gridLayout_3.addWidget(self.comboBoxFunction1, 0, 1, 1, 1)

        self.comboBoxValue1 = QComboBox(self.groupBoxValues)
        self.comboBoxValue1.setObjectName(u"comboBoxValue1")

        self.gridLayout_3.addWidget(self.comboBoxValue1, 0, 0, 1, 1)

        self.comboBoxSort2 = QComboBox(self.groupBoxValues)
        self.comboBoxSort2.setObjectName(u"comboBoxSort2")

        self.gridLayout_3.addWidget(self.comboBoxSort2, 2, 2, 1, 1)

        self.comboBoxSort1 = QComboBox(self.groupBoxValues)
        self.comboBoxSort1.setObjectName(u"comboBoxSort1")

        self.gridLayout_3.addWidget(self.comboBoxSort1, 0, 2, 1, 1)

        self.comboBoxFunction2 = QComboBox(self.groupBoxValues)
        self.comboBoxFunction2.setObjectName(u"comboBoxFunction2")

        self.gridLayout_3.addWidget(self.comboBoxFunction2, 2, 1, 1, 1)

        self.comboBoxValue2 = QComboBox(self.groupBoxValues)
        self.comboBoxValue2.setObjectName(u"comboBoxValue2")

        self.gridLayout_3.addWidget(self.comboBoxValue2, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)


        self.verticalLayout_3.addWidget(self.groupBoxValues)

        self.groupBoxRow = QGroupBox(AnalysisWidget)
        self.groupBoxRow.setObjectName(u"groupBoxRow")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxRow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.comboBoxRow1 = QComboBox(self.groupBoxRow)
        self.comboBoxRow1.setObjectName(u"comboBoxRow1")

        self.gridLayout_2.addWidget(self.comboBoxRow1, 0, 0, 1, 1)

        self.lineEditRow1 = QLineEdit(self.groupBoxRow)
        self.lineEditRow1.setObjectName(u"lineEditRow1")

        self.gridLayout_2.addWidget(self.lineEditRow1, 0, 1, 1, 1)

        self.comboBoxRow2 = QComboBox(self.groupBoxRow)
        self.comboBoxRow2.setObjectName(u"comboBoxRow2")

        self.gridLayout_2.addWidget(self.comboBoxRow2, 1, 0, 1, 1)

        self.lineEditRow2 = QLineEdit(self.groupBoxRow)
        self.lineEditRow2.setObjectName(u"lineEditRow2")

        self.gridLayout_2.addWidget(self.lineEditRow2, 1, 1, 1, 1)

        self.comboBoxRow3 = QComboBox(self.groupBoxRow)
        self.comboBoxRow3.setObjectName(u"comboBoxRow3")

        self.gridLayout_2.addWidget(self.comboBoxRow3, 2, 0, 1, 1)

        self.lineEditRow3 = QLineEdit(self.groupBoxRow)
        self.lineEditRow3.setObjectName(u"lineEditRow3")

        self.gridLayout_2.addWidget(self.lineEditRow3, 2, 1, 1, 1)

        self.comboBoxRow4 = QComboBox(self.groupBoxRow)
        self.comboBoxRow4.setObjectName(u"comboBoxRow4")

        self.gridLayout_2.addWidget(self.comboBoxRow4, 3, 0, 1, 1)

        self.lineEditRow4 = QLineEdit(self.groupBoxRow)
        self.lineEditRow4.setObjectName(u"lineEditRow4")

        self.gridLayout_2.addWidget(self.lineEditRow4, 3, 1, 1, 1)

        self.comboBoxRow5 = QComboBox(self.groupBoxRow)
        self.comboBoxRow5.setObjectName(u"comboBoxRow5")

        self.gridLayout_2.addWidget(self.comboBoxRow5, 4, 0, 1, 1)

        self.lineEditRow5 = QLineEdit(self.groupBoxRow)
        self.lineEditRow5.setObjectName(u"lineEditRow5")

        self.gridLayout_2.addWidget(self.lineEditRow5, 4, 1, 1, 1)

        self.comboBoxRow6 = QComboBox(self.groupBoxRow)
        self.comboBoxRow6.setObjectName(u"comboBoxRow6")

        self.gridLayout_2.addWidget(self.comboBoxRow6, 5, 0, 1, 1)

        self.lineEditRow6 = QLineEdit(self.groupBoxRow)
        self.lineEditRow6.setObjectName(u"lineEditRow6")

        self.gridLayout_2.addWidget(self.lineEditRow6, 5, 1, 1, 1)

        self.comboBoxRow7 = QComboBox(self.groupBoxRow)
        self.comboBoxRow7.setObjectName(u"comboBoxRow7")

        self.gridLayout_2.addWidget(self.comboBoxRow7, 6, 0, 1, 1)

        self.lineEditRow7 = QLineEdit(self.groupBoxRow)
        self.lineEditRow7.setObjectName(u"lineEditRow7")

        self.gridLayout_2.addWidget(self.lineEditRow7, 6, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 36, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.groupBoxRow)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBoxColumn = QGroupBox(AnalysisWidget)
        self.groupBoxColumn.setObjectName(u"groupBoxColumn")
        self.groupBoxColumn.setEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxColumn)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.comboBoxColumn1 = QComboBox(self.groupBoxColumn)
        self.comboBoxColumn1.setObjectName(u"comboBoxColumn1")

        self.gridLayout.addWidget(self.comboBoxColumn1, 0, 0, 1, 1)

        self.comboBoxColumn2 = QComboBox(self.groupBoxColumn)
        self.comboBoxColumn2.setObjectName(u"comboBoxColumn2")

        self.gridLayout.addWidget(self.comboBoxColumn2, 0, 1, 1, 1)

        self.comboBoxColumn3 = QComboBox(self.groupBoxColumn)
        self.comboBoxColumn3.setObjectName(u"comboBoxColumn3")

        self.gridLayout.addWidget(self.comboBoxColumn3, 0, 2, 1, 1)

        self.lineEditColumn1 = QLineEdit(self.groupBoxColumn)
        self.lineEditColumn1.setObjectName(u"lineEditColumn1")

        self.gridLayout.addWidget(self.lineEditColumn1, 1, 0, 1, 1)

        self.lineEditColumn2 = QLineEdit(self.groupBoxColumn)
        self.lineEditColumn2.setObjectName(u"lineEditColumn2")

        self.gridLayout.addWidget(self.lineEditColumn2, 1, 1, 1, 1)

        self.lineEditColumn3 = QLineEdit(self.groupBoxColumn)
        self.lineEditColumn3.setObjectName(u"lineEditColumn3")

        self.gridLayout.addWidget(self.lineEditColumn3, 1, 2, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalSpacer = QSpacerItem(38, 17, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addWidget(self.groupBoxColumn)

        self.tableView = EnhancedTableView(AnalysisWidget)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_5.addWidget(self.tableView)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonShowApply = QPushButton(AnalysisWidget)
        self.pushButtonShowApply.setObjectName(u"pushButtonShowApply")
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        self.pushButtonShowApply.setFont(font)
        self.pushButtonShowApply.setStyleSheet(u"QPushButton#pushButtonShowApply {\n"
"	border: 2px solid blue;\n"
"	border-radius: 5px;\n"
"	padding: 4px 8px;\n"
"}")

        self.horizontalLayout_3.addWidget(self.pushButtonShowApply)

        self.label_2 = QLabel(AnalysisWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.comboBoxAnalysis = QComboBox(AnalysisWidget)
        self.comboBoxAnalysis.setObjectName(u"comboBoxAnalysis")

        self.horizontalLayout_3.addWidget(self.comboBoxAnalysis)

        self.label = QLabel(AnalysisWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.comboBoxEvent = QComboBox(AnalysisWidget)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.horizontalLayout_3.addWidget(self.comboBoxEvent)

        self.checkBoxTotal = QCheckBox(AnalysisWidget)
        self.checkBoxTotal.setObjectName(u"checkBoxTotal")

        self.horizontalLayout_3.addWidget(self.checkBoxTotal)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)


        self.retranslateUi(AnalysisWidget)

        QMetaObject.connectSlotsByName(AnalysisWidget)
    # setupUi

    def retranslateUi(self, AnalysisWidget):
        AnalysisWidget.setWindowTitle(QCoreApplication.translate("AnalysisWidget", u"Form", None))
        self.groupBoxValues.setTitle(QCoreApplication.translate("AnalysisWidget", u"Values", None))
        self.groupBoxRow.setTitle(QCoreApplication.translate("AnalysisWidget", u"Row", None))
        self.groupBoxColumn.setTitle(QCoreApplication.translate("AnalysisWidget", u"Column", None))
        self.pushButtonShowApply.setText(QCoreApplication.translate("AnalysisWidget", u"Apply/Refresh", None))
        self.label_2.setText(QCoreApplication.translate("AnalysisWidget", u"Analysis", None))
        self.label.setText(QCoreApplication.translate("AnalysisWidget", u"Event:", None))
        self.checkBoxTotal.setText(QCoreApplication.translate("AnalysisWidget", u"Totals", None))
    # retranslateUi

