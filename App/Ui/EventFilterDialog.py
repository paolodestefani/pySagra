# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EventFilterDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDateEdit,
    QDialog, QDialogButtonBox, QGroupBox, QHBoxLayout,
    QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_EventFilterDialog(object):
    def setupUi(self, EventFilterDialog):
        if not EventFilterDialog.objectName():
            EventFilterDialog.setObjectName(u"EventFilterDialog")
        EventFilterDialog.resize(280, 281)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EventFilterDialog.sizePolicy().hasHeightForWidth())
        EventFilterDialog.setSizePolicy(sizePolicy)
        EventFilterDialog.setMinimumSize(QSize(280, 0))
        self.verticalLayout_4 = QVBoxLayout(EventFilterDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBoxEvent = QGroupBox(EventFilterDialog)
        self.groupBoxEvent.setObjectName(u"groupBoxEvent")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxEvent)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.comboBoxEvent = QComboBox(self.groupBoxEvent)
        self.comboBoxEvent.setObjectName(u"comboBoxEvent")

        self.verticalLayout_2.addWidget(self.comboBoxEvent)


        self.verticalLayout_4.addWidget(self.groupBoxEvent)

        self.groupBoxDate = QGroupBox(EventFilterDialog)
        self.groupBoxDate.setObjectName(u"groupBoxDate")
        self.groupBoxDate.setCheckable(True)
        self.groupBoxDate.setChecked(False)
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxDate)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.dateEditDate = QDateEdit(self.groupBoxDate)
        self.dateEditDate.setObjectName(u"dateEditDate")
        self.dateEditDate.setCalendarPopup(True)

        self.verticalLayout_3.addWidget(self.dateEditDate)


        self.verticalLayout_4.addWidget(self.groupBoxDate)

        self.groupBoxDayPart = QGroupBox(EventFilterDialog)
        self.groupBoxDayPart.setObjectName(u"groupBoxDayPart")
        self.groupBoxDayPart.setCheckable(True)
        self.groupBoxDayPart.setChecked(False)
        self.verticalLayout = QVBoxLayout(self.groupBoxDayPart)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButtonLunch = QRadioButton(self.groupBoxDayPart)
        self.radioButtonLunch.setObjectName(u"radioButtonLunch")
        self.radioButtonLunch.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButtonLunch)

        self.radioButtonDinner = QRadioButton(self.groupBoxDayPart)
        self.radioButtonDinner.setObjectName(u"radioButtonDinner")

        self.horizontalLayout_2.addWidget(self.radioButtonDinner)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addWidget(self.groupBoxDayPart)

        self.verticalSpacer = QSpacerItem(20, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(EventFilterDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_4.addWidget(self.buttonBox)


        self.retranslateUi(EventFilterDialog)
        self.buttonBox.accepted.connect(EventFilterDialog.accept)
        self.buttonBox.rejected.connect(EventFilterDialog.reject)

        QMetaObject.connectSlotsByName(EventFilterDialog)
    # setupUi

    def retranslateUi(self, EventFilterDialog):
        EventFilterDialog.setWindowTitle(QCoreApplication.translate("EventFilterDialog", u"Event filter dialog", None))
        self.groupBoxEvent.setTitle(QCoreApplication.translate("EventFilterDialog", u"Event", None))
        self.groupBoxDate.setTitle(QCoreApplication.translate("EventFilterDialog", u"Date", None))
        self.groupBoxDayPart.setTitle(QCoreApplication.translate("EventFilterDialog", u"Day part", None))
        self.radioButtonLunch.setText(QCoreApplication.translate("EventFilterDialog", u"Lunch", None))
        self.radioButtonDinner.setText(QCoreApplication.translate("EventFilterDialog", u"Dinner", None))
    # retranslateUi

