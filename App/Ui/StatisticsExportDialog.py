# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StatisticsExportDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_StatisticsExportDialog(object):
    def setupUi(self, StatisticsExportDialog):
        if not StatisticsExportDialog.objectName():
            StatisticsExportDialog.setObjectName(u"StatisticsExportDialog")
        StatisticsExportDialog.resize(459, 268)
        self.verticalLayout_3 = QVBoxLayout(StatisticsExportDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(StatisticsExportDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(StatisticsExportDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditHeadersFileName = QLineEdit(StatisticsExportDialog)
        self.lineEditHeadersFileName.setObjectName(u"lineEditHeadersFileName")

        self.gridLayout.addWidget(self.lineEditHeadersFileName, 0, 1, 1, 1)

        self.pushButtonSelectHeaders = QPushButton(StatisticsExportDialog)
        self.pushButtonSelectHeaders.setObjectName(u"pushButtonSelectHeaders")

        self.gridLayout.addWidget(self.pushButtonSelectHeaders, 0, 2, 1, 1)

        self.label_4 = QLabel(StatisticsExportDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEditDetailsFileName = QLineEdit(StatisticsExportDialog)
        self.lineEditDetailsFileName.setObjectName(u"lineEditDetailsFileName")

        self.gridLayout.addWidget(self.lineEditDetailsFileName, 1, 1, 1, 1)

        self.pushButtonSelectDetails = QPushButton(StatisticsExportDialog)
        self.pushButtonSelectDetails.setObjectName(u"pushButtonSelectDetails")

        self.gridLayout.addWidget(self.pushButtonSelectDetails, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.checkBoxIncludeAll = QCheckBox(StatisticsExportDialog)
        self.checkBoxIncludeAll.setObjectName(u"checkBoxIncludeAll")

        self.verticalLayout.addWidget(self.checkBoxIncludeAll)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBoxFromEvent = QGroupBox(StatisticsExportDialog)
        self.groupBoxFromEvent.setObjectName(u"groupBoxFromEvent")
        self.verticalLayout_8 = QVBoxLayout(self.groupBoxFromEvent)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBoxFromEvent = QComboBox(self.groupBoxFromEvent)
        self.comboBoxFromEvent.setObjectName(u"comboBoxFromEvent")

        self.verticalLayout_8.addWidget(self.comboBoxFromEvent)


        self.horizontalLayout.addWidget(self.groupBoxFromEvent)

        self.groupBoxToEvent = QGroupBox(StatisticsExportDialog)
        self.groupBoxToEvent.setObjectName(u"groupBoxToEvent")
        self.verticalLayout_9 = QVBoxLayout(self.groupBoxToEvent)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.comboBoxToEvent = QComboBox(self.groupBoxToEvent)
        self.comboBoxToEvent.setObjectName(u"comboBoxToEvent")

        self.verticalLayout_9.addWidget(self.comboBoxToEvent)


        self.horizontalLayout.addWidget(self.groupBoxToEvent)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(17, 11, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(StatisticsExportDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_3.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEditHeadersFileName, self.pushButtonSelectHeaders)
        QWidget.setTabOrder(self.pushButtonSelectHeaders, self.lineEditDetailsFileName)
        QWidget.setTabOrder(self.lineEditDetailsFileName, self.pushButtonSelectDetails)
        QWidget.setTabOrder(self.pushButtonSelectDetails, self.checkBoxIncludeAll)
        QWidget.setTabOrder(self.checkBoxIncludeAll, self.comboBoxFromEvent)
        QWidget.setTabOrder(self.comboBoxFromEvent, self.comboBoxToEvent)

        self.retranslateUi(StatisticsExportDialog)
        self.buttonBox.accepted.connect(StatisticsExportDialog.accept)
        self.buttonBox.rejected.connect(StatisticsExportDialog.reject)

        QMetaObject.connectSlotsByName(StatisticsExportDialog)
    # setupUi

    def retranslateUi(self, StatisticsExportDialog):
        StatisticsExportDialog.setWindowTitle(QCoreApplication.translate("StatisticsExportDialog", u"Statistics export", None))
        self.labelIcon.setText(QCoreApplication.translate("StatisticsExportDialog", u"Icon", None))
        self.label.setText(QCoreApplication.translate("StatisticsExportDialog", u"Headers file", None))
        self.pushButtonSelectHeaders.setText(QCoreApplication.translate("StatisticsExportDialog", u"Select ...", None))
        self.label_4.setText(QCoreApplication.translate("StatisticsExportDialog", u"Details file", None))
        self.pushButtonSelectDetails.setText(QCoreApplication.translate("StatisticsExportDialog", u"Select ...", None))
        self.checkBoxIncludeAll.setText(QCoreApplication.translate("StatisticsExportDialog", u"Include ALL events", None))
        self.groupBoxFromEvent.setTitle(QCoreApplication.translate("StatisticsExportDialog", u"From event", None))
        self.groupBoxToEvent.setTitle(QCoreApplication.translate("StatisticsExportDialog", u"To event", None))
    # retranslateUi

