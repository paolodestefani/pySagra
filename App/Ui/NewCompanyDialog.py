# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NewCompanyDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

from App.Widget.Control import RelationalComboBox

class Ui_NewCompanyDialog(object):
    def setupUi(self, NewCompanyDialog):
        if not NewCompanyDialog.objectName():
            NewCompanyDialog.setObjectName(u"NewCompanyDialog")
        NewCompanyDialog.resize(512, 480)
        self.verticalLayout_9 = QVBoxLayout(NewCompanyDialog)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.groupBox_2 = QGroupBox(NewCompanyDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.spinBoxCode = QSpinBox(self.groupBox_2)
        self.spinBoxCode.setObjectName(u"spinBoxCode")
        self.spinBoxCode.setMinimum(1)
        self.spinBoxCode.setMaximum(9999)

        self.verticalLayout_3.addWidget(self.spinBoxCode)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(NewCompanyDialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lineEditDescription = QLineEdit(self.groupBox_3)
        self.lineEditDescription.setObjectName(u"lineEditDescription")

        self.verticalLayout_4.addWidget(self.lineEditDescription)


        self.horizontalLayout_3.addWidget(self.groupBox_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.groupBox_5 = QGroupBox(NewCompanyDialog)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)

        self.comboBoxProfile = RelationalComboBox(self.groupBox_5)
        self.comboBoxProfile.setObjectName(u"comboBoxProfile")

        self.gridLayout.addWidget(self.comboBoxProfile, 1, 0, 1, 1)

        self.comboBoxMenu = RelationalComboBox(self.groupBox_5)
        self.comboBoxMenu.setObjectName(u"comboBoxMenu")

        self.gridLayout.addWidget(self.comboBoxMenu, 1, 1, 1, 1)

        self.comboBoxToolbar = RelationalComboBox(self.groupBox_5)
        self.comboBoxToolbar.setObjectName(u"comboBoxToolbar")

        self.gridLayout.addWidget(self.comboBoxToolbar, 1, 2, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout)


        self.verticalLayout_8.addWidget(self.groupBox_5)

        self.groupBox = QGroupBox(NewCompanyDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelImage = QLabel(self.groupBox)
        self.labelImage.setObjectName(u"labelImage")
        self.labelImage.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelImage)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButtonUpload = QPushButton(self.groupBox)
        self.pushButtonUpload.setObjectName(u"pushButtonUpload")

        self.verticalLayout.addWidget(self.pushButtonUpload)

        self.verticalSpacer = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButtonClear = QPushButton(self.groupBox)
        self.pushButtonClear.setObjectName(u"pushButtonClear")

        self.verticalLayout.addWidget(self.pushButtonClear)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(NewCompanyDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout_8.addWidget(self.buttonBox)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBoxProfile)
        self.label_2.setBuddy(self.comboBoxProfile)
        self.label_3.setBuddy(self.comboBoxProfile)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(NewCompanyDialog)
        self.buttonBox.accepted.connect(NewCompanyDialog.accept)
        self.buttonBox.rejected.connect(NewCompanyDialog.reject)

        QMetaObject.connectSlotsByName(NewCompanyDialog)
    # setupUi

    def retranslateUi(self, NewCompanyDialog):
        NewCompanyDialog.setWindowTitle(QCoreApplication.translate("NewCompanyDialog", u"New company", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("NewCompanyDialog", u"Code", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("NewCompanyDialog", u"Description", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("NewCompanyDialog", u"Current user access settings to new company", None))
        self.label.setText(QCoreApplication.translate("NewCompanyDialog", u"Profile", None))
        self.label_2.setText(QCoreApplication.translate("NewCompanyDialog", u"Menu", None))
        self.label_3.setText(QCoreApplication.translate("NewCompanyDialog", u"Toolbar", None))
        self.groupBox.setTitle(QCoreApplication.translate("NewCompanyDialog", u"Company image", None))
        self.labelImage.setText(QCoreApplication.translate("NewCompanyDialog", u"NO IMAGE", None))
        self.pushButtonUpload.setText(QCoreApplication.translate("NewCompanyDialog", u"Upload...", None))
        self.pushButtonClear.setText(QCoreApplication.translate("NewCompanyDialog", u"Clear", None))
    # retranslateUi

