# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AdaptationsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
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
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AdaptationsDialog(object):
    def setupUi(self, AdaptationsDialog):
        if not AdaptationsDialog.objectName():
            AdaptationsDialog.setObjectName(u"AdaptationsDialog")
        AdaptationsDialog.resize(320, 200)
        self.verticalLayout_4 = QVBoxLayout(AdaptationsDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelIcon = QLabel(AdaptationsDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_2.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.groupBox_5 = QGroupBox(AdaptationsDialog)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout = QVBoxLayout(self.groupBox_5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBoxItemView = QCheckBox(self.groupBox_5)
        self.checkBoxItemView.setObjectName(u"checkBoxItemView")

        self.verticalLayout.addWidget(self.checkBoxItemView)

        self.checkBoxSortFilter = QCheckBox(self.groupBox_5)
        self.checkBoxSortFilter.setObjectName(u"checkBoxSortFilter")

        self.verticalLayout.addWidget(self.checkBoxSortFilter)

        self.checkBoxReport = QCheckBox(self.groupBox_5)
        self.checkBoxReport.setObjectName(u"checkBoxReport")

        self.verticalLayout.addWidget(self.checkBoxReport)


        self.horizontalLayout.addWidget(self.groupBox_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButtonExport = QPushButton(AdaptationsDialog)
        self.pushButtonExport.setObjectName(u"pushButtonExport")
        self.pushButtonExport.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonExport)

        self.pushButtonImport = QPushButton(AdaptationsDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")
        self.pushButtonImport.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonImport)

        self.pushButtonClear = QPushButton(AdaptationsDialog)
        self.pushButtonClear.setObjectName(u"pushButtonClear")
        self.pushButtonClear.setAutoDefault(False)

        self.verticalLayout_3.addWidget(self.pushButtonClear)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(AdaptationsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.retranslateUi(AdaptationsDialog)
        self.buttonBox.accepted.connect(AdaptationsDialog.accept)
        self.buttonBox.rejected.connect(AdaptationsDialog.reject)

        QMetaObject.connectSlotsByName(AdaptationsDialog)
    # setupUi

    def retranslateUi(self, AdaptationsDialog):
        AdaptationsDialog.setWindowTitle(QCoreApplication.translate("AdaptationsDialog", u"Dialog", None))
        self.labelIcon.setText(QCoreApplication.translate("AdaptationsDialog", u"Icon", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("AdaptationsDialog", u"Adaptation type", None))
        self.checkBoxItemView.setText(QCoreApplication.translate("AdaptationsDialog", u"ItemView", None))
        self.checkBoxSortFilter.setText(QCoreApplication.translate("AdaptationsDialog", u"SortFilter", None))
        self.checkBoxReport.setText(QCoreApplication.translate("AdaptationsDialog", u"Report", None))
        self.pushButtonExport.setText(QCoreApplication.translate("AdaptationsDialog", u"Export", None))
        self.pushButtonImport.setText(QCoreApplication.translate("AdaptationsDialog", u"Import", None))
        self.pushButtonClear.setText(QCoreApplication.translate("AdaptationsDialog", u"Clear", None))
    # retranslateUi

