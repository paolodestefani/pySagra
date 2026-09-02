# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EventToolDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_EventToolDialog(object):
    def setupUi(self, EventToolDialog):
        if not EventToolDialog.objectName():
            EventToolDialog.setObjectName(u"EventToolDialog")
        EventToolDialog.resize(512, 342)
        self.verticalLayout_6 = QVBoxLayout(EventToolDialog)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.labelIcon = QLabel(EventToolDialog)
        self.labelIcon.setObjectName(u"labelIcon")

        self.verticalLayout_4.addWidget(self.labelIcon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBoxUtility = QGroupBox(EventToolDialog)
        self.groupBoxUtility.setObjectName(u"groupBoxUtility")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxUtility)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.comboBoxUtility = QComboBox(self.groupBoxUtility)
        self.comboBoxUtility.setObjectName(u"comboBoxUtility")

        self.verticalLayout_2.addWidget(self.comboBoxUtility)


        self.verticalLayout_5.addWidget(self.groupBoxUtility)

        self.groupBoxWarning = QGroupBox(EventToolDialog)
        self.groupBoxWarning.setObjectName(u"groupBoxWarning")
        font = QFont()
        font.setBold(True)
        self.groupBoxWarning.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBoxWarning)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelWarning = QLabel(self.groupBoxWarning)
        self.labelWarning.setObjectName(u"labelWarning")
        font1 = QFont()
        font1.setBold(False)
        self.labelWarning.setFont(font1)
        self.labelWarning.setWordWrap(True)

        self.verticalLayout.addWidget(self.labelWarning)


        self.verticalLayout_5.addWidget(self.groupBoxWarning)

        self.groupBoxEvent = QGroupBox(EventToolDialog)
        self.groupBoxEvent.setObjectName(u"groupBoxEvent")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxEvent)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.comboBoxEvent = QComboBox(self.groupBoxEvent)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout_3.addWidget(self.comboBoxEvent)


        self.verticalLayout_5.addWidget(self.groupBoxEvent)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(EventToolDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Close|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_6.addWidget(self.buttonBox)


        self.retranslateUi(EventToolDialog)
        self.buttonBox.accepted.connect(EventToolDialog.accept)
        self.buttonBox.rejected.connect(EventToolDialog.reject)

        QMetaObject.connectSlotsByName(EventToolDialog)
    # setupUi

    def retranslateUi(self, EventToolDialog):
        EventToolDialog.setWindowTitle(QCoreApplication.translate("EventToolDialog", u"Event tool", None))
        self.labelIcon.setText(QCoreApplication.translate("EventToolDialog", u"Icon", None))
        self.groupBoxUtility.setTitle(QCoreApplication.translate("EventToolDialog", u"Utiity", None))
        self.groupBoxWarning.setTitle(QCoreApplication.translate("EventToolDialog", u"Warning", None))
        self.labelWarning.setText(QCoreApplication.translate("EventToolDialog", u"Utility text", None))
        self.groupBoxEvent.setTitle(QCoreApplication.translate("EventToolDialog", u"Event", None))
    # retranslateUi

